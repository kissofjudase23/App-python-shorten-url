from typing import List

from abc import abstractmethod

from shorten_url.models.mixin import EntitryMixin
from shorten_url.pattern import SingletonABCMeta


class UserEntitry(EntitryMixin):

    def __init__(self, name, email, id=None):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return f'[' \
               f'<id:{self.id}>\n' \
               f'<cid:{self.name}>\n' \
               f'<uid:{self.email}>\n' \
               f']'


class UserRepositoryABC(metaclass=SingletonABCMeta):
    @abstractmethod
    def add_user(self, name, email):
        """ add a new user

        Args:
        Return:
            user_id
        Raise :
            DuplicateUserError
        """
        raise NotImplementedError()

    @abstractmethod
    def list_users(self, page, page_size) -> List[UserEntitry]:
        """ List the users

        Args:
            offset = page * page_size
            limit = page_size
        Return:
            List[UserEntitry]
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_user(self, user_id):
        raise NotImplementedError()
