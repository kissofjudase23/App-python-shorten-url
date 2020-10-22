from abc import abstractmethod
from typing import List
from shorten_url.pattern import SingletonABCMeta


class UrlEntity(object):

    __slots__ = ["entity"]

    def __init__(self, base62_id, ori_url):
        self.entity = {"base62_id": base62_id, "ori_url": ori_url}

    @property
    def asdict(self) -> dict:
        return self.entity

    @property
    def id(self):
        return self.entity["base62_id"]

    def __repr__(self):
        return str(self.entity)

    def __eq__(self, other):
        return self.asdict["base62_id"] == other.asdict["base62_id"]

    def __lt__(self, other):
        return self.asdict["base62_id"] < other.asdict["base62_id"]

    def __le__(self, other):
        return self.asdict["base62_id"] <= other.asdict["base62_id"]


class UrlRepositoryABC(metaclass=SingletonABCMeta):
    @abstractmethod
    def add_url(self, user_id, ori_url) -> str:
        """Add a new url
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
    def delete_url(self, user_id, base62_url_id):
        """Add a new url
        Args:
            user_id
            base62_url_id
        Return:
        Raises:
            NoUrlFoundError
        """
        raise NotImplementedError()

    @abstractmethod
    def get_ori_url(self, base62_url_id) -> str:
        """Get the original URL
        Args:
            base62_url_id
        Return:
            ori_url
        Raise:
            NoUrlFoundError
        """
        raise NotImplementedError()

    @abstractmethod
    def list_urls(self, user_id, page, page_size) -> List[UrlEntity]:
        raise NotImplementedError()

    @abstractmethod
    def delete_urls(self, ori_url_pattern):
        """Get the original URL
        Args:
            base62_url_id
        Return:
            ori_url
        """
        raise NotImplementedError()
