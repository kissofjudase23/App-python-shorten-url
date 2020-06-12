
from shorten_url.variables import DbTypes
from shorten_url.models.user import UserRepositoryABC
from shorten_url.storages import Repositories
import pytest


@pytest.fixture
def user_repo(scope="class"):
    user_repo = Repositories.user(DbTypes.MYSQL.value)
    yield user_repo


@pytest.mark.mysql_user_repo
class TestUserRepo(object):

    @pytest.mark.parametrize("user, email", [
        pytest.param("tes1", "test1@gmail.com"),
        pytest.param("tes2", "test2@gmail.com")]
    )
    def test_add_users(self,
                       user_repo: UserRepositoryABC, user, email):
        uid = user_repo.add_user(user, email)
        assert uid >= 1
        user_repo.delete_user(uid)
