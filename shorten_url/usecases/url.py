from typing import List

from shorten_url.pattern import Singleton
from shorten_url.models.url import UrlRepositoryABC, UrlEntity
from shorten_url.models.cache import CacheRepositoryABC


def marshal_url_entities(url_entities: List[UrlEntity]) -> List[dict]:
    return [e.asdict for e in url_entities]


class Url(metaclass=Singleton):

    CACHE_EX_GET_ORI_URL = 60
    CACHE_EX_LIST_URLS = 60

    def __init__(self, url_repo: UrlRepositoryABC = None, cache: CacheRepositoryABC = None):

        self._url_repo = url_repo
        self._cache = cache

    @property
    def url_repo(self) -> UrlRepositoryABC:
        return self._url_repo

    @url_repo.setter
    def url_repo(self, url_repo: UrlRepositoryABC):
        self._url_repo = url_repo

    @property
    def cache(self) -> CacheRepositoryABC:
        return self._cache

    @cache.setter
    def cache(self, cache: CacheRepositoryABC):
        self._cache = cache

    @staticmethod
    def get_get_ori_url_key(base62_url_id):
        return f"Url:get_ori_url:{base62_url_id}"

    @staticmethod
    def get_list_urls_key(user_id):
        return f"Url:list_urls:{user_id}"

    def add_url(self, user_id, ori_url) -> str:
        """Add a new url
        Args:
            user_id
            ori_url
        Return:
            shorten_url_address
        Raises:
            NoUserFoundError
            DuplicateUrlError
        """
        b62_url_id = self._url_repo.add_url(user_id, ori_url)
        return b62_url_id

    def delete_url(self, user_id, base62_url_id):
        """Add a new url
        Args:
            user_id
            base62_url_id
        Return:
        Raises:
            NoUrlFoundError
        """
        self._url_repo.delete_url(user_id, base62_url_id)

    def list_urls(self, user_id, page=0, page_size=100) -> List[dict]:
        """Add a new url
        Args:
            user_id
        Return:
            List[UrlEntity]
        Raises:
        """
        cache_key = self.get_list_urls_key(user_id)
        cache_result = self._cache.get_json(key=cache_key)
        if cache_result:
            return cache_result

        url_entities = self._url_repo.list_urls(user_id, page, page_size)
        marshalled_result = marshal_url_entities(url_entities)
        # marshal_user_entities
        self._cache.set_json(key=cache_key, val=marshalled_result, ex=self.CACHE_EX_LIST_URLS)

        return marshalled_result

    def get_ori_url(self, base62_url_id) -> str:
        """Get the original URL
        Args:
            base62_url_id
        Return:
            ori_url
        Raise:
            NoUrlFoundError
        """
        cache_key = self.get_get_ori_url_key(base62_url_id)
        cache_result = self._cache.get(key=cache_key)
        if cache_result:
            return cache_result

        ori_url = self._url_repo.get_ori_url(base62_url_id)

        self._cache.set(key=cache_key, val=ori_url, ex=self.CACHE_EX_GET_ORI_URL)
        return ori_url
