from abc import abstractmethod
from shorten_url.pattern import SingletonABCMeta


class UrlEntity(object):

    __slots__ = ['entity']

    def __init__(self, base62_id, ori_url):
        self.entity = {"base62_id": base62_id,
                       "ori_url": ori_url}


class UrlRepositoryABC(metaclass=SingletonABCMeta):

    @abstractmethod
    def add_url(self, user_id, ori_url) -> str:
        """ Add a new url
        Args:
            user_id
            ori_url
        Return:
            base62_url_id
        Raises:
            NoUserFoundError
            DuplicateUrlError
        """
        raise NotImplementedError()

    @abstractmethod
    def get_ori_url(self, base62_url_id) -> str:
        """ Get the original URL
        Args:
            base62_url_id
        Return:
            ori_url
        Raise:
            NoUrlFoundError
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_urls(self, ori_url_pattern):
        """ Get the original URL
        Args:
            base62_url_id
        Return:
            ori_url
        """
        raise NotImplementedError()
