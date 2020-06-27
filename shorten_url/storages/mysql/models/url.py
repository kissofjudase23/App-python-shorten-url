import base62
from typing import List
from sqlalchemy.orm import load_only
from sqlalchemy import and_


from sqlalchemy import exc as sqla_exc

from shorten_url.models.url import UrlRepositoryABC, UrlEntity
from shorten_url.storages.mysql.db import transaction_context
from shorten_url.storages.mysql.tables.user import User
from shorten_url.storages.mysql.tables.url import Url
from shorten_url.storages.mysql.tables.user_url_map import UserUrlMap
import shorten_url.exc as exc


def to_base62_id(id_: int) -> str:
    return base62.encode(id_)


def to_int_id(base62_id: str) -> int:
    return base62.decode(base62_id)


class MysqlUrlRepo(UrlRepositoryABC):

    def add_url(self, user_id, ori_url) -> str:
        """ Add a new url
        Args:
            user_id
            ori_url
        Return:
            base62_url_id
        """
        user_id = int(user_id)
        with transaction_context() as session:
            # add the new url record
            url = Url(ori_url=ori_url)
            session.add(url)
            try:
                session.commit()
            except sqla_exc.IntegrityError:
                session.rollback()
                # the url may be created by other user
                # don't need to raise here
                pass

            # get the url id
            url = session.query(Url)\
                         .options(load_only(Url.id))\
                         .filter(Url.ori_url == ori_url).one()
            url_id = url.id
            try:
                # add user_url_map
                user_url_map = UserUrlMap(user_id, url_id)
                session.add(user_url_map)
                session.commit()
            except sqla_exc.IntegrityError:
                raise exc.DuplicateUrlError("The user url mapping has been created before")

        return to_base62_id(url_id)

    def delete_url(self, user_id, base62_url_id):
        """ Add a new url
        Args:
            user_id
            base62_url_id
        Return:
        Raises:
            NoUrlFoundError
        """
        try:
            url_id = to_int_id(base62_url_id)
        except Exception:
            raise exc.NoUrlFoundError(f"{base62_url_id} is not a valid base62_url_id")

        with transaction_context() as session:
            session.query(UserUrlMap)\
                   .filter(and_(UserUrlMap.user_id == user_id, UserUrlMap.url_id == url_id))\
                   .delete(synchronize_session=False)

    def get_ori_url(self, base62_url_id) -> str:
        """ Get the original URL
        Args:
            base62_url_id
        Return:
            ori_url
        Raise:
            NoUserFoundError
        """
        try:
            url_id = to_int_id(base62_url_id)
        except Exception:
            raise exc.NoUrlFoundError(f"{base62_url_id} is not a valid base62_url_id")

        with transaction_context() as session:
            url = session.query(Url)\
                         .options(load_only(Url.ori_url))\
                         .filter(Url.id == url_id).one_or_none()
            if not url:
                raise exc.NoUrlFoundError(f"{base62_url_id} not found")

            return url.ori_url

    def list_urls(self, user_id, page=0, page_size=100) -> List[UrlEntity]:
        url_entities = []
        user_id = int(user_id)
        with transaction_context() as session:
            query = session.query(User)\
                           .join(UserUrlMap, User.id == UserUrlMap.user_id)\
                           .join(Url, UserUrlMap.url_id == Url.id)\
                           .with_entities(Url.id, Url.ori_url)\
                           .filter(User.id == user_id)\

            if page and page_size:
                query = query.offset(page * page_size)

            if page_size:
                query = query.limit(page_size)

            """
            Result is a list of tuples
            [ (1, 'https://google.com.tw/123'),
              (2, 'https://google.com.tw/456') ]
            """
            for url_id, ori_url in query.all():
                url_entities.append(UrlEntity(base62_id=to_base62_id(url_id),
                                              ori_url=ori_url))

        return url_entities

    def delete_urls(self, ori_url_pattern=None):
        with transaction_context() as session:
            query = session.query(Url)
            if ori_url_pattern:
                query = query.filter(Url.ori_url.like(ori_url_pattern))
            query.delete(synchronize_session=False)


def test():
    # from pprint import pprint as pp
    from shorten_url.storages.mysql.models.user import MysqlUserRepo

    user_repo = MysqlUserRepo()
    url_repo = MysqlUrlRepo()

    user_uid = user_repo.add_user(name="Tom", email="5566")
    print(f"user_uid:{user_uid}")

    base62_url_id = url_repo.add_url(user_id=user_uid,
                                     ori_url="https://google.com.tw/123")
    print(f"base62_url_id:{base62_url_id}")

    base62_url_id = url_repo.add_url(user_id=user_uid,
                                     ori_url="https://google.com.tw/456")
    print(f"base62_url_id:{base62_url_id}")

    user_uid = "1"
    url_entities = url_repo.list_urls(user_uid)
    for entity in url_entities:
        print(entity)


if __name__ == "__main__":
    test()
