from shorten_url.models.cache import CacheRepositoryABC
from shorten_url.variables import CacheVars
import redis


class RedisCache(CacheRepositoryABC):
    # Ref: https://redis-py.readthedocs.io/en/latest/

    def __init__(
        self, host=CacheVars.HOST, port=CacheVars.PORT, *, max_connections=CacheVars.MAX_CONNECTIONS
    ):

        self.redis = redis.Redis(
            host=host,
            port=port,
            max_connections=max_connections,
            encoding="utf-8",
            decode_responses=True,
        )

    def set(self, key, val, *, ex=None):
        self.redis.set(key, val, ex)

    def get(self, key):
        return self.redis.get(key)

    def delete(self, *key):
        self.redis.delete(*key)
