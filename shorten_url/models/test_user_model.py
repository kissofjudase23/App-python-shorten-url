
from shorten_url.variables import DbTypes
from shorten_url.models.user import UserRepositoryABC, UserEntitry
from shorten_url.storages import Repositories
import shorten_url.exc as exc
import pytest


TEST_USER_PREFIX = "testuser"


@pytest.fixture
def user_repo(scope="function") -> UserRepositoryABC:
    user_repo = Repositories.user(DbTypes.MYSQL.value)
    yield user_repo
    user_repo.delete_users(user_name_pattern=f"{TEST_USER_PREFIX}%")


test_users = [
    (f"{TEST_USER_PREFIX}1", "test1@gmail.com"),
    (f"{TEST_USER_PREFIX}20000000000", "test2@gmail.commmmmmmmmmmmmmmmmmmmmmmmm")
]


@pytest.mark.mysql
@pytest.mark.user_repo
class TestUserRepo(object):

    @pytest.mark.parametrize("name, email", test_users)
    def test_add_users(self,
                       user_repo: UserRepositoryABC,
                       name, email):
        uid = user_repo.add_user(name, email)
        assert uid >= 1

    @pytest.mark.parametrize("name, email", test_users)
    def test_add_user_duplicate(self,
                                user_repo: UserRepositoryABC,
                                name, email):
        user_repo.add_user(name, email)
        with pytest.raises(exc.DuplicateUserError):
            user_repo.add_user(name, email)

    @pytest.mark.parametrize("name, email", test_users)
    def test_check_if_the_user_exist(self,
                                     user_repo: UserRepositoryABC,
                                     name, email):
        user_id = user_repo.add_user(name, email)
        actual = user_repo.is_the_user_exist(user_id)
        assert actual is True

        user_repo.delete_user(user_id)
        actual = user_repo.is_the_user_exist(user_id)
        assert actual is False

    @pytest.mark.parametrize("name, email", test_users)
    def test_get_user_info(self,
                           user_repo: UserRepositoryABC,
                           name, email):

        user_id = user_repo.add_user(name, email)
        expected = UserEntitry(name=name, email=email, id=user_id)
        actual = user_repo.get_user_info(user_id)
        assert actual == expected

    def test_list_users(self,
                        user_repo: UserRepositoryABC):

        expected = []
        for name, email in test_users:
            user_id = user_repo.add_user(name, email)
            expected.append(UserEntitry(name=name, email=email, id=user_id))

        actual = user_repo.list_users(0, 100)
        assert sorted(expected) == sorted(actual)
