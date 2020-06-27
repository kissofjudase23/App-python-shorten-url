

from shorten_url.pattern import Singleton
from shorten_url.models.url import UrlRepositoryABC
from shorten_url.cache.abc import CacheABC


class Url(metaclass=Singleton):

    CACHE_EX_GET_ORI_URL = 60

    def __init__(self,
                 url_repo: UrlRepositoryABC = None,
                 cache: CacheABC = None):

        self._url_repo = url_repo
        self._cache = cache

    @property
    def url_repo(self) -> UrlRepositoryABC:
        return self._url_repo

    @url_repo.setter
    def url_repo(self, url_repo: UrlRepositoryABC):
        self._url_repo = url_repo

    @property
    def cache(self) -> CacheABC:
        return self._cache

    @cache.setter
    def cache(self, cache: CacheABC):
        self._cache = cache

    @staticmethod
    def get_get_ori_url_key(base62_url_id):
        return f"Url:get_ori_url:{base62_url_id}"

    def add_url(self, user_id, ori_url) -> str:
        """ Add a new url
        Args:
            user_id
            ori_url
        Return:
            shorten_url_address
        Raise:
            NoUserFoundError
            DuplicateUrlError
        """
        b62_url_id = self._url_repo.add_url(user_id, ori_url)
        return b62_url_id

    def get_ori_url(self, base62_url_id) -> str:
        """ Get the original URL
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

        self._cache.set(key=cache_key,
                        val=ori_url,
                        ex=self.CACHE_EX_GET_ORI_URL)
        return ori_url
