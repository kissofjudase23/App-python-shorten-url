from unittest import mock

import pytest
import base62

from shorten_url.models.cache import CacheRepositoryABC
from shorten_url.models.url import UrlRepositoryABC
from shorten_url.usecases.url import Url


test_base62_url_ids = [
    (base62.encode(1), "http://google.com.tw/123"),
    (base62.encode(2), "http://google.com.tw/456"),
    (base62.encode(3), "http://google.com.tw/789"),
]


@pytest.fixture
def url_usecases(scope="class"):
    url_usecases = Url()
    yield url_usecases


@pytest.mark.usecases
@pytest.mark.url_usecases
class TestUrlUseCases(object):
    @pytest.mark.parametrize("base62_url_id, ori_url", test_base62_url_ids)
    def test_get_ori_url(self, url_usecases: Url, base62_url_id, ori_url):

        # create and set the mock object
        mock_url_repo = mock.create_autospec(UrlRepositoryABC)
        mock_cache = mock.create_autospec(CacheRepositoryABC)
        url_usecases.cache = mock_cache
        url_usecases.url_repo = mock_url_repo

        # mock the return values
        mock_cache.get.return_value = None
        mock_url_repo.get_ori_url.return_value = ori_url

        # check results
        actual = url_usecases.get_ori_url(base62_url_id)
        assert actual == ori_url

        # check assert calls
        mock_url_repo.get_ori_url.assert_called_once_with(base62_url_id)

        cache_key = Url.get_get_ori_url_key(base62_url_id)
        mock_cache.get.assert_called_once_with(key=cache_key)
        mock_cache.set.assert_called_once_with(
            key=cache_key, val=ori_url, ex=Url.CACHE_EX_GET_ORI_URL
        )

    @pytest.mark.parametrize("base62_url_id, ori_url", test_base62_url_ids)
    def test_get_ori_url_use_cache(self, url_usecases: Url, base62_url_id, ori_url):

        # create and set the mock object
        mock_url_repo = mock.create_autospec(UrlRepositoryABC)
        mock_cache = mock.create_autospec(CacheRepositoryABC)
        url_usecases.cache = mock_cache
        url_usecases.url_repo = mock_url_repo

        # mock the return values
        mock_cache.get.return_value = ori_url

        # check results
        actual = url_usecases.get_ori_url(base62_url_id)
        assert actual == ori_url

        # check assert calls
        cache_key = Url.get_get_ori_url_key(base62_url_id)
        mock_cache.get.assert_called_once_with(key=cache_key)

        mock_url_repo.get_ori_url.assert_not_called()
        mock_cache.set.assert_not_called()
