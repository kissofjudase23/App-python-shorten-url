import base62
from sqlalchemy.orm import load_only


from sqlalchemy import exc as sqla_exc

from shorten_url.models.url import UrlRepositoryABC
from shorten_url.storages.mysql.db import transaction_context
from shorten_url.storages.mysql.tables.url import Url
from shorten_url.storages.mysql.tables.user_url_map import UserUrlMap
import shorten_url.exc as exc


class Base62Encorder(object):
    @staticmethod
    def to_base62_id(id):
        return base62.encode(int(id))

    @staticmethod
    def to_id(base62_id):
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
        with transaction_context() as session:
            # add the new url record
            try:
                url = Url(ori_url=ori_url)
                session.add(url)
            except sqla_exc.IntegrityError:
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

        return Base62Encorder.to_base62_id(url_id)

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
            url_id = Base62Encorder.to_id(base62_url_id)
        except Exception:
            raise exc.NoUrlFoundError(f"{base62_url_id} is not a valid base62_url_id")

        with transaction_context() as session:
            url = session.query(Url)\
                         .options(load_only(Url.ori_url))\
                         .filter(Url.id == url_id).one_or_none()
            if not url:
                raise exc.NoUrlFoundError(f"{base62_url_id} not found")

            return url.ori_url

    def delete_all_urls(self):
        with transaction_context() as session:
            session.query(Url).delete()


def test():
    # from pprint import pprint as pp
    from shorten_url.storages.mysql.models.user import MysqlUserRepo

    user_repo = MysqlUserRepo()
    url_repo = MysqlUrlRepo()

    user_uid = user_repo.add_user(name="Tom", email="5566")
    print(f"user_uid:{user_uid}")

    base62_url_id = url_repo.add_url(user_id=user_uid,
                                     ori_url="https://google.com.tw")
    print(f"base62_url_id:{base62_url_id}")

    ori_url = url_repo.get_ori_url(base62_url_id)
    print(f"ori_url:{ori_url}")


if __name__ == "__main__":
    test()