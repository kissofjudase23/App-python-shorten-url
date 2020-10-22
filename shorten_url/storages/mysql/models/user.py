from typing import List

from sqlalchemy import exc as sqla_exc
from sqlalchemy.orm import load_only

from shorten_url.models.user import UserEntity, UserRepositoryABC
from shorten_url.storages.mysql.db import transaction_context
from shorten_url.storages.mysql.tables.user import User
import shorten_url.exc as exc


def to_user_entitry(user: User) -> UserEntity:
    return UserEntity(name=user.name, email=user.email, id=user.id)


class MysqlUserRepo(UserRepositoryABC):
    def add_user(self, name, email) -> str:
        with transaction_context() as session:
            user = User(name, email)
            session.add(user)
            try:
                session.commit()
            except sqla_exc.IntegrityError as e:
                raise exc.DuplicateUserError(f"{e}") from e
            return str(user.id)

    def list_users(self, page=0, page_size=100) -> List[UserEntity]:
        with transaction_context() as session:
            users = []

            query = session.query(User).options(load_only(User.id, User.name, User.email))

            if page and page_size:
                query = query.offset(page * page_size)

            if page_size:
                query = query.limit(page_size)

            for record in query.all():
                users.append(to_user_entitry(record))

            return users

    def get_user_info(self, user_id) -> UserEntity:
        user_id = int(user_id)
        with transaction_context() as session:
            record = (
                session.query(User)
                .options(load_only(User.id, User.name, User.email))
                .filter(User.id == user_id)
                .one_or_none()
            )
            if not record:
                raise exc.NoUserFoundError(f"user:{user_id} not found")
            return to_user_entitry(record)

    def is_the_user_exist(self, user_id) -> bool:
        user_id = int(user_id)
        with transaction_context() as session:
            record = (
                session.query(User)
                .options(load_only(User.id))
                .filter(User.id == user_id)
                .one_or_none()
            )
            return True if record else False

    def delete_user(self, user_id):
        user_id = int(user_id)
        with transaction_context() as session:
            session.query(User).filter(User.id == user_id).delete(synchronize_session=False)

    def delete_users(self, user_name_pattern=None):
        """
        user_name_pattern:testuser%
                          %testuser%
        """
        with transaction_context() as session:
            query = session.query(User)
            if user_name_pattern:
                query = query.filter(User.name.like(user_name_pattern))
            query.delete(synchronize_session=False)


def test():
    from pprint import pprint as pp

    user_repo = MysqlUserRepo()
    uid = user_repo.add_user(name="testuser1", email="5566")
    uid = user_repo.add_user(name="testuser2", email="7788")
    pp(user_repo.list_users())
    pp(user_repo.get_user_info(uid))
    user_repo.delete_users(user_name_pattern="testuser%")


if __name__ == "__main__":
    test()
