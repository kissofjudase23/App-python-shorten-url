from shorten_url.variables import DbVars

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager

# import models
# https://stackoverflow.com/questions/7478403/sqlalchemy-classes-across-files
# To break the cyclic import, take Base out of the module that imports A, B and C;
from shorten_url.storages.mysql.tables.base import BASE
import shorten_url.storages.mysql.tables.user
import shorten_url.storages.mysql.tables.url
import shorten_url.storages.mysql.tables.user_url_map

from shorten_url.storages.mysql.vars import CHARSET, DRIVER

ECHO_RAW_SQL_COMMAND = False


def create_db_url(host,
                  port,
                  db,
                  username,
                  password,
                  *,
                  db_charset='utf8mb4',
                  driver='pymysql'):
    url = f'mysql+{driver}://{username}:{password}@{host}:{port}/{db}?charset={db_charset}'
    return url


class DbEngine(object):
    URL = create_db_url(host=DbVars.HOST,
                        port=DbVars.PORT,
                        db=DbVars.DATABASE,
                        username=DbVars.USER,
                        password=DbVars.PASSWORD,
                        db_charset=CHARSET,
                        driver=DRIVER)

    ENGINE = create_engine(URL,
                           pool_size=DbVars.MAX_CONNECTIONS,
                           encoding="utf8",
                           echo=ECHO_RAW_SQL_COMMAND)

    _ = BASE.metadata.create_all(bind=ENGINE,
                                 checkfirst=True)

    SESSION = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=True,
                                          bind=ENGINE))

    BASE.query = SESSION.query_property()


@contextmanager
def transaction_context():
    session = DbEngine.SESSION()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        DbEngine.SESSION.remove()
