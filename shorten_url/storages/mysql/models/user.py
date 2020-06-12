from typing import List

from sqlalchemy import exc as sqla_exc

from shorten_url.models.user import UserEntitry, UserRepositoryABC
from shorten_url.storages.mysql.db import transaction_context
from shorten_url.storages.mysql.tables.user import User
import shorten_url.exc as exc


def to_user_entitry(user: User) -> UserEntitry:
    return UserEntitry(name=user.name,
                       email=user.email,
                       id=user.id)


class MysqlUserRepo(UserRepositoryABC):
    def add_user(self, name, email):
        try:
            with transaction_context() as session:
                user = User(name, email)
                session.add(user)

            user_id = None
            with transaction_context() as session:
                user = session.query(User)\
                              .with_entities(User.id)\
                              .filter(User.email == email).one()
                user_id = user.id

            return user_id

        except sqla_exc.IntegrityError as e:
            raise exc.DuplicateUserError(f"{e}") from e

    def list_users(self, page=0, page_size=100) -> List[UserEntitry]:
        with transaction_context() as session:
            users = []

            query = session.query(User)

            if page and page_size:
                query = query.offset(page * page_size)

            if page_size:
                query = query.limit(page_size)

            for record in query.all():
                users.append(to_user_entitry(record))

            return users

    def get_user_info(self, user_id) -> UserEntitry:
        with transaction_context() as session:
            record = session.query(User)\
                            .filter(User.id == user_id).one_or_none()
            if not record:
                raise exc.UserNotFoundError(f"user for {user_id} not found")

            return to_user_entitry(record)

    def delete_user(self, user_id):
        with transaction_context() as session:
            session.query(User).filter(User.id == user_id).delete()

    def delete_all_users(self):
        with transaction_context() as session:
            session.query(User).delete()


def test():
    from pprint import pprint as pp
    user_repo = MysqlUserRepo()
    user_repo.add_user(name="Tom", email="5566")
    pp(user_repo.list_users(page=0, page_size=100))
    user_repo.delete_all_users()


if __name__ == "__main__":
    test()
