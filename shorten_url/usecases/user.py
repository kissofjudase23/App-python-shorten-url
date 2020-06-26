from typing import List
from shorten_url.pattern import Singleton
from shorten_url.models.user import UserRepositoryABC, UserEntitry
from shorten_url.cache.abc import CacheABC


def marshal_user_entities(user_entitries: List[UserEntitry]) -> List[dict]:
    m_entitries = []

    for entity in user_entitries:
        m_entitries.append(entity.asdict)

    return m_entitries


class User(metaclass=Singleton):

    def __init__(self,
                 user_repo: UserRepositoryABC = None,
                 cache: CacheABC = None):

        self._user_repo = user_repo
        self._cache = cache

    @property
    def user_repo(self) -> UserRepositoryABC:
        return self._user_repo

    @user_repo.setter
    def user_repo(self, user_repo: UserRepositoryABC):
        self._user_repo = user_repo

    @property
    def cache(self) -> CacheABC:
        return self._cache

    @cache.setter
    def cache(self, cache: CacheABC):
        self._cache = cache

    def add_user(self, name, email):
        """ add a new user
        Args:
        Return:
            user_id
        Raise :
            DuplicateUserError
        """
        return self._user_repo.add_user(name, email)

    def list_users(self, page=0, page_size=100) -> List[dict]:
        """ List the users
        Args:
            offset = page * page_size
            limit = page_size
        Return:
            List[UserEntitry]
        """
        cache_key = f"User:list_users:{page}:{page_size}"
        cache_result = self._cache.get_json(cache_key)
        if cache_result:
            return cache_result

        user_entities = self._user_repo.list_users(page, page_size)
        marshalled_result = marshal_user_entities(user_entities)

        # marshal_user_entities
        cache_ex = 10
        self._cache.set_json(key=cache_key,
                             val=marshalled_result,
                             ex=cache_ex)
        return marshalled_result

    def delete_user(self, user_id):
        return self._user_repo.delete_user(user_id)

    def get_user_info(self, user_id) -> dict:
        """ Get the user information
        Args:
        Raise :
            NoUserFoundError
        """
        cache_key = f"User:get_user_info:{user_id}"
        cache_result = self._cache.get_json(cache_key)
        if cache_result:
            return cache_result

        user_entity = self._user_repo.get_user_info(user_id)
        cache_ex = 10
        self._cache.set_json(key=cache_key,
                             val=user_entity.asdict,
                             ex=cache_ex)

        return user_entity.asdict
