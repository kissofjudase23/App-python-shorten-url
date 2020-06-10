

class AppError(ValueError):
    """ App Base Error
    """
    pass


class ConfigError(AppError):
    pass


class EnvVariableMissing(ConfigError):
    pass


class NotSupportedEnvVariable(ConfigError):
    pass


class DataBaseError(AppError):
    pass


class DuplicateUserError(DataBaseError):
    pass
