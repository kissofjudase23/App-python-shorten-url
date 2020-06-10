from shorten_url.cache.abc import CacheABC
from shorten_url.variables import CacheVars
import redis


class RedisCache(CacheABC):

    def __init__(self,
                 host=CacheVars.HOST,
                 port=CacheVars.PORT,
                 *,
                 max_connections=CacheVars.MAX_CONNECTIONS):

        self.redis = redis.Redis(host=host,
                                 port=port,
                                 max_connections=max_connections,
                                 encoding="utf-8",
                                 decode_responses=True)

    def set(self, key, val, *, ex=None):
        self.redis.set(key, val, ex)

    def get(self, key):
        return self.redis.get(key)