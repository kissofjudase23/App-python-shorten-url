import pytest
import time

from shorten_url.variables import CacheTypes
from shorten_url.models.cache import CacheRepositoryABC
from shorten_url.storages import Repositories


@pytest.fixture
def cache(scope="class") -> CacheRepositoryABC:
    cache = Repositories.cache(CacheTypes.REDIS.value)
    yield cache


test_kvs = [
    ("test:key1", "test_5566"),
    ("test:key2", "test_7788_00000000000000000000000000000000000000000000000000"),
    ("test:key300000000000000000000000000", "test_7788_00000000000000000000000000000000000000000000000000"),
    ("test:key4empty", "")
]

test_json_kvs = [
    ("test:key1_json", {"key1": "data1", "key2": "data2", "key3": "data3"}),
    ("test:key2_json_empty_dict", {}),
    ("test:key3_json_empty_list", [])
]


@pytest.mark.redis
class TestRedis(object):

    @pytest.mark.parametrize("key, val", test_kvs)
    def test_set_key(self,
                     cache: CacheRepositoryABC,
                     key,
                     val,
                     ex=5):
        cache.set(key, val, ex=ex)
        actual = cache.get(key)
        assert actual == val

    @pytest.mark.parametrize("key, val", test_kvs)
    def test_delete_key(self,
                        cache: CacheRepositoryABC,
                        key,
                        val,
                        ex=None):

        cache.set(key, val, ex=ex)
        actual = cache.get(key)
        assert actual == val

        cache.delete(key)
        actual = cache.get(key)
        assert actual is None

    @pytest.mark.parametrize("key, val", test_json_kvs)
    def test_set_json_key(self,
                          cache: CacheRepositoryABC,
                          key,
                          val,
                          ex=5):

        cache.set_json(key, val, ex=ex)
        actual = cache.get_json(key)
        assert actual == val

    @pytest.mark.parametrize("key, val, ex", [
        pytest.param("test:key1_ex", "test_ex_val_5566", 2)]
    )
    def test_set_key_expire(self,
                            cache: CacheRepositoryABC,
                            key, val, ex):

        cache.set(key, val, ex=ex)
        time.sleep(ex + 1)
        actual = cache.get(key)
        assert actual is None
