from typing import List
from shorten_url.pattern import Singleton
from shorten_url.models.user import UserRepositoryABC, UserEntitry
from shorten_url.cache.abc import CacheABC


class User(metaclass=Singleton):

    def __init__(self,
                 user_repo: UserRepositoryABC,
                 cache: CacheABC):

        self.user_repo = user_repo
        self.cache = cache

    def add_user(self, name, email):
        """ add a new user
        Args:
        Return:
            user_id
        Raise :
            DuplicateUserError
        """
        return self.user_repo.add_user(name, email)

    def list_users(self, page=0, page_size=100) -> List[UserEntitry]:
        """ List the users

        Args:
            offset = page * page_size
            limit = page_size
        Return:
            List[UserEntitry]
        """
        cache_key = f"User:list_users:{page}:{page_size}"
        cache_ex = 300

        cache_result = self.cache.get_json(cache_key)
        if cache_result:
            return cache_result

        result = self.user_repo.add_user(page, page_size)
        self.cache.set_json(key=cache_key, val=result, ex=cache_ex)
        return result

    def delete_user(self, user_id):
        return self.user_repo.delete_user(user_id)
