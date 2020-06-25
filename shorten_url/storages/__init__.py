from shorten_url.variables import DbVars, DbTypes
from unittest import mock


class Repositories(object):

    @classmethod
    def user(cls, db_type=DbVars.TYPE):
        if db_type == DbTypes.MYSQL.value:
            from shorten_url.storages.mysql.models.user import MysqlUserRepo
            return MysqlUserRepo()

        elif db_type == DbTypes.MOCK.value:
            from shorten_url.models.user import UserRepositoryABC
            return mock.create_autospec(UserRepositoryABC)

        raise NotImplementedError(f"Does not support {db_type}")

    @classmethod
    def url(cls, db_type=DbVars.TYPE):
        if db_type == DbTypes.MYSQL.value:
            from shorten_url.storages.mysql.models.url import MysqlUrlRepo
            return MysqlUrlRepo()

        elif db_type == DbTypes.MOCK.value:
            from shorten_url.models.url import UrlRepositoryABC
            return mock.create_autospec(UrlRepositoryABC)

        raise NotImplementedError(f"Does not support {db_type}")