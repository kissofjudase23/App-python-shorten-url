import pytest
import time

from shorten_url.variables import CacheTypes
from shorten_url.cache.abc import CacheABC
from shorten_url.cache import get_cache


@pytest.fixture
def cache(scope="class") -> CacheABC:
    cache = get_cache(CacheTypes.REDIS.value)
    yield cache


@pytest.mark.redis
class TestRedis(object):

    @pytest.mark.parametrize("key, val", [
        pytest.param("test:key1", "test_5566"),
        pytest.param("test:key2", "test_7788_00000000000000000000000000000000000000000000000000")]
    )
    def test_set_key(self,
                     cache: CacheABC,
                     key, val, ex=600):
        cache.set(key, val, ex=ex)
        actual = cache.get(key)
        assert actual == val

    @pytest.mark.parametrize("key, val", [
        pytest.param("test:key1_json", {"key1": "data1", "key2": "data2", "key3": "data3"}),
        pytest.param("test:key2_json", {})]
    )
    def test_set_json_key(self,
                          cache: CacheABC,
                          key, val, ex=600):
        cache.set_json(key, val, ex=ex)
        actual = cache.get_json(key)
        assert actual == val

    @pytest.mark.parametrize("key, val, ex", [
        pytest.param("test:key1_ex", "test_ex_val_5566", 2)]
    )
    def test_set_key_expire(self,
                            cache: CacheABC,
                            key, val, ex):

        cache.set(key, val, ex=ex)
        time.sleep(ex + 1)
        actual = cache.get(key)
        assert actual is None
