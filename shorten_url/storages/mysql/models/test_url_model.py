
from shorten_url.variables import DbTypes
from shorten_url.models.url import UrlRepositoryABC
from shorten_url.storages import Repositories
import shorten_url.exc as exc
import pytest


TEST_URL_PREFIX = "https://test.domain.com"
TEST_USER = "test_user_for_url_add"
TEST_EMAIL = "test_user_for_url_add@gmail.com"


@pytest.fixture
def url_repo(scope="function") -> UrlRepositoryABC:
    url_repo = Repositories.url(DbTypes.MYSQL.value)
    yield url_repo
    url_repo.delete_urls(f"{TEST_URL_PREFIX}%")


@pytest.fixture
def user_id(scope="class") -> str:
    user_repo = Repositories.user(DbTypes.MYSQL.value)
    user_id = user_repo.add_user(TEST_USER, TEST_EMAIL)
    yield user_id
    user_repo.delete_user(user_id)


test_urlrs = [
    (f"{TEST_URL_PREFIX}/123"),
    (f"{TEST_URL_PREFIX}/456"),
    (f"{TEST_URL_PREFIX}/111111111111/8888888888888888")
]


@pytest.mark.mysql
@pytest.mark.mysql_url_repo
class TestUrlRepo(object):

    @pytest.mark.parametrize("ori_url", test_urlrs)
    def test_add_url(self,
                     url_repo: UrlRepositoryABC,
                     user_id,
                     ori_url):

        base_64_url_id = url_repo.add_url(user_id=user_id, ori_url=ori_url)
        actual = url_repo.get_ori_url(base_64_url_id)
        expected = ori_url
        assert expected == actual

    @pytest.mark.parametrize("ori_url", test_urlrs)
    def test_add_duplicated_urls(self,
                                 url_repo: UrlRepositoryABC,
                                 user_id,
                                 ori_url):

        url_repo.add_url(user_id=user_id, ori_url=ori_url)
        # caused by user_url_map
        with pytest.raises(exc.DuplicateUrlError):
            url_repo.add_url(user_id=user_id, ori_url=ori_url)
