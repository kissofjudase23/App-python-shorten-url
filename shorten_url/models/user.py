from typing import List
from abc import abstractmethod

from shorten_url.pattern import SingletonABCMeta


class UserEntitry(object):

    __slots__ = ['entity']

    def __init__(self, name, email, id=None):
        self.entity = {"id": id,
                       "name": name,
                       "email": email}

    @property
    def asdict(self) -> dict:
        return self.entity

    @property
    def id(self):
        return self.entity['id']

    @property
    def name(self):
        return self.entity['name']

    @name.setter
    def name(self, new_name):
        self.entity['name'] = new_name

    @property
    def email(self):
        return self.entity['email']

    def __repr__(self):
        return str(self.entity)


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
    def check_if_the_user_exist(self, user_id) -> bool:
        """ Check if the usr exists
        Return:
            True
            False
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_user(self, user_id):
        raise NotImplementedError()

    @abstractmethod
    def get_user_info(self, user_id) -> UserEntitry:
        """
        Raise:
            NoUserFoundError
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_all_users(self):
        """ Waining: Delte all users in the table
        """
        raise NotImplementedError()
