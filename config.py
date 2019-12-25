from os import getenv


class Config():
    FLASK_ENV = getenv('FLASK_ENV')
    DB_URI = getenv('DB_URI')
    DB_MAX_POOL_SIZE = int(getenv('DB_MAX_POOL_SIZE', 10))
    SECRET_KEY = getenv('SECRET_KEY')


class DevConfig(Config):
    DEBUG = True


class TestConfig(DevConfig):
    TESTING = True


def get_config(env=getenv('FLASK_ENV')):
    return {
        "testing": TestConfig,
        "development": DevConfig,
        "production": Config
    }.get(env, Config)
