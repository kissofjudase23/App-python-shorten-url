from enum import Enum
from distutils.util import strtobool
import os
from shorten_url import exc


class DbTypes(Enum):
    MOCK = "mock"
    MYSQL = "mysql"


class CacheTypes(Enum):
    MOCK = "mock"
    REDIS = "redis"


SUPPORTED_DB_TYPES = tuple(enum.value for enum in DbTypes)
SUPPORTED_CACHE_TYPES = tuple(enum.value for enum in CacheTypes)


def get_os_env(key, check_list=None):
    if key not in os.environ:
        raise exc.EnvVariableMissing(f"cat not find {key} in os.env")

    val = os.environ[key]

    if check_list and val not in check_list:
        raise exc.NotSupportedEnvVariable(f"do not support {val} for {key}")

    return os.environ[key]


class AppVars(object):
    HOST = get_os_env("APP_HOST")
    ENABLE_SWAGGER = strtobool(get_os_env(key="APP_ENABLE_SWAGGER"))


class DbVars(object):
    TYPE = get_os_env(key="DB_TYPE", check_list=SUPPORTED_DB_TYPES)
    HOST = get_os_env("DB_HOST")
    PORT = int(get_os_env("DB_PORT"))
    MAX_CONNECTIONS = int(get_os_env("DB_MAX_CONNECTIONS"))
    DATABASE = get_os_env("DB_DATABASE")
    USER = get_os_env("DB_USER")
    PASSWORD = get_os_env("DB_PASSWORD")


class CacheVars(object):
    TYPE = get_os_env(key="CACHE_TYPE", check_list=SUPPORTED_CACHE_TYPES)
    HOST = get_os_env("CACHE_HOST")
    PORT = int(get_os_env("CACHE_PORT"))
    MAX_CONNECTIONS = int(get_os_env("CACHE_MAX_CONNECTIONS"))
