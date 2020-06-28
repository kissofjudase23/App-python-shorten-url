from shorten_url.variables import (DbVars,
                                   DbTypes,
                                   CacheVars,
                                   CacheTypes)
from shorten_url.models.cache import CacheRepositoryABC
from unittest import mock


class Repositories(object):

    @classmethod
    def user(cls, db_type=DbVars.TYPE):
        if db_type == DbTypes.MYSQL.value:
            from shorten_url.storages.mysql.models.user import MysqlUserRepo
            return MysqlUserRepo()

        elif db_type == DbTypes.MOCK.value:
            from shorten_url.models.user import UserRepositoryABC
            return mock.create_autospec(UserRepositoryABC)

        raise NotImplementedError(f"Does not support {db_type}")

    @classmethod
    def url(cls, db_type=DbVars.TYPE):
        if db_type == DbTypes.MYSQL.value:
            from shorten_url.storages.mysql.models.url import MysqlUrlRepo
            return MysqlUrlRepo()

        elif db_type == DbTypes.MOCK.value:
            from shorten_url.models.url import UrlRepositoryABC
            return mock.create_autospec(UrlRepositoryABC)

        raise NotImplementedError(f"Does not support {db_type}")

    @classmethod
    def cache(cls, cache_type=CacheVars.TYPE) -> CacheRepositoryABC:
        if cache_type == CacheTypes.REDIS.value:
            from shorten_url.storages.redis.cache import RedisCache
            return RedisCache()

        elif cache_type == CacheTypes.MOCK.value:
            return mock.create_autospec(CacheRepositoryABC)

        raise NotImplementedError(f"Does not support {cache_type}")