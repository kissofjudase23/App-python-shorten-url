from shorten_url.variables import DbTypes
from shorten_url.models.user import UserEntitry, UserRepositoryABC
from shorten_url.cache import CacheABC
from shorten_url.usecases.user import User
import pytest
from unittest import mock


@pytest.fixture
def user_usecases(scope="class"):
    user_usecases = User()
    yield user_usecases


test_user_ids = [
    ("0"),
    ("55555"),
    ("999999999"),
    ("1000000000000000000000000000000000")
]


@pytest.mark.usecases
@pytest.mark.user_usecases
class TestUserUseCases(object):

    @pytest.mark.parametrize("user_id", test_user_ids)
    def test_get_user_info_use_cache(self,
                                     user_usecases: User,
                                     user_id):

        # create and set the mock objects
        mock_user_repo = mock.create_autospec(UserRepositoryABC)
        mock_cache = mock.create_autospec(CacheABC)
        user_usecases.user_repo = mock_user_repo
        user_usecases.cache = mock_cache

        # mock the return value
        expected = cache_result = UserEntitry(id=user_id,
                                              name="tom",
                                              email="tom@gamil.com").asdict
        mock_cache.get_json.return_value = cache_result

        # check results
        actual = user_usecases.get_user_info(user_id)
        assert actual == expected

        # check assert calls
        mock_cache.set_json.assert_not_called()
        mock_user_repo.get_user_info.assert_not_called()

    @pytest.mark.parametrize("user_id", test_user_ids)
    def test_get_user_info_do_not_use_cache(self,
                                            user_usecases: User,
                                            user_id):

        # create and set the mock objects
        mock_user_repo = mock.create_autospec(UserRepositoryABC)
        mock_cache = mock.create_autospec(CacheABC)
        user_usecases.user_repo = mock_user_repo
        user_usecases.cache = mock_cache

        # mock the return value
        mock_cache.get_json.return_value = None
        user_entity = UserEntitry(id=user_id, name="tom", email="tom@gamil.com")
        mock_user_repo.get_user_info.return_value = user_entity

        # check results
        expected = user_entity.asdict
        actual = user_usecases.get_user_info(user_id)
        assert actual == expected

        # check assert calls
        mock_user_repo.get_user_info.assert_called_once_with(user_id)
        mock_cache.set_json.assert_called_once_with(key=user_usecases.get_user_info_key(user_id),
                                                    val=user_entity.asdict,
                                                    ex=user_usecases.CACHE_EX_GET_USER_INFO)
