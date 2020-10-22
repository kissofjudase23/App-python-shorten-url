from typing import List
from unittest import mock

import pytest

from shorten_url.models.user import UserEntity, UserRepositoryABC
from shorten_url.models.cache import CacheRepositoryABC
from shorten_url.usecases.user import User


@pytest.fixture
def user_usecases(scope="class"):
    user_usecases = User()
    yield user_usecases


test_user_ids = [("0"), ("55555"), ("999999999"), ("1000000000000000000000000000000000")]

test_user_entities = [
    (
        [
            UserEntity(name="Tom", email="Tom@gmail.com", id="1"),
            UserEntity(name="Emily", email="Emily@gmail.com", id="2"),
            UserEntity(name="Jason", email="Jason@gmail.com", id="3"),
        ]
    )
]


@pytest.mark.usecases
@pytest.mark.user_usecases
class TestUserUseCases(object):
    @pytest.mark.parametrize("user_id", test_user_ids)
    def test_get_user_info_use_cache(self, user_usecases: User, user_id):

        # create and set the mock objects
        mock_user_repo = mock.create_autospec(UserRepositoryABC)
        mock_cache = mock.create_autospec(CacheRepositoryABC)
        user_usecases.user_repo = mock_user_repo
        user_usecases.cache = mock_cache

        # mock the return value
        expected = cache_result = UserEntity(id=user_id, name="tom", email="tom@gamil.com").asdict
        mock_cache.get_json.return_value = cache_result

        # check results
        actual = user_usecases.get_user_info(user_id)
        assert actual == expected

        # check assert calls
        mock_cache.set_json.assert_not_called()
        mock_user_repo.get_user_info.assert_not_called()

    @pytest.mark.parametrize("user_id", test_user_ids)
    def test_get_user_info_(self, user_usecases: User, user_id):

        # create and set the mock objects
        mock_user_repo = mock.create_autospec(UserRepositoryABC)
        mock_cache = mock.create_autospec(CacheRepositoryABC)
        user_usecases.user_repo = mock_user_repo
        user_usecases.cache = mock_cache

        # mock the return value
        mock_cache.get_json.return_value = None
        user_entity = UserEntity(id=user_id, name="tom", email="tom@gamil.com")
        mock_user_repo.get_user_info.return_value = user_entity

        # check results
        expected = user_entity.asdict
        actual = user_usecases.get_user_info(user_id)
        assert actual == expected

        # check assert calls
        mock_user_repo.get_user_info.assert_called_once_with(user_id)

        cache_key = user_usecases.get_user_info_key(user_id)
        mock_cache.get_json.assert_called_once_with(key=cache_key)
        mock_cache.set_json.assert_called_once_with(
            key=cache_key, val=user_entity.asdict, ex=user_usecases.CACHE_EX_GET_USER_INFO
        )

    @pytest.mark.parametrize("user_entities", test_user_entities)
    def test_list_users_use_cache(
        self, user_usecases: User, user_entities: List[UserEntity], page=0, page_size=100
    ):

        # create and set the mock objects
        mock_user_repo = mock.create_autospec(UserRepositoryABC)
        mock_cache = mock.create_autospec(CacheRepositoryABC)
        user_usecases.user_repo = mock_user_repo
        user_usecases.cache = mock_cache

        # mock the return value
        expected = [e.asdict for e in user_entities]
        mock_cache.get_json.return_value = expected

        # check results
        actual = user_usecases.list_users(page, page_size)
        assert actual == expected

        # check assert calls
        cache_key = User.get_list_users_key(page, page_size)
        mock_cache.get_json.assert_called_once_with(key=cache_key)

        mock_cache.set_json.assert_not_called()
        mock_user_repo.list_users.assert_not_called()

    @pytest.mark.parametrize("user_entities", test_user_entities)
    def test_list_users(
        self, user_usecases: User, user_entities: List[UserEntity], page=0, page_size=100
    ):

        # create and set the mock objects
        mock_user_repo = mock.create_autospec(UserRepositoryABC)
        mock_cache = mock.create_autospec(CacheRepositoryABC)
        user_usecases.user_repo = mock_user_repo
        user_usecases.cache = mock_cache

        # mock the return value
        mock_cache.get_json.return_value = None
        mock_user_repo.list_users.return_value = user_entities

        # check results
        expected = [e.asdict for e in user_entities]
        actual = user_usecases.list_users(page, page_size)
        assert actual == expected

        # check assert calls
        mock_user_repo.list_users.assert_called_once_with(page, page_size)

        cache_key = User.get_list_users_key(page, page_size)
        mock_cache.get_json.assert_called_once_with(key=cache_key)
        mock_cache.set_json.assert_called_once_with(
            key=cache_key, val=expected, ex=User.CACHE_EX_LIST_USERS
        )
