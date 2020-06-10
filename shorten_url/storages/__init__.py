from shorten_url.variables import DbVars, DbTypes
from shorten_url.models.user import UserRepositoryABC
from unittest import mock


class Repositories(object):

    @classmethod
    def user(cls, db_type=DbVars.TYPE):
        if db_type == DbTypes.MYSQL.value:
            from shorten_url.storages.mysql.models.user import MysqlUserRepo
            return MysqlUserRepo()

        elif db_type == DbTypes.MOCK.value:
            return mock.create_autospec(UserRepositoryABC)

        raise NotImplementedError(f"Does not support {db_type}")