from shorten_url.variables import CacheVars, CacheTypes
from shorten_url.cache.abc import CacheABC
from unittest import mock


def get_cache(cache_type=CacheVars.TYPE) -> CacheABC:

    if cache_type == CacheTypes.REDIS.value:
        from shorten_url.cache.redis import RedisCache
        return RedisCache()

    elif cache_type == CacheTypes.MOCK.value:
        return mock.create_autospec(CacheABC)

    raise NotImplementedError(f"Does not support {cache_type}")
