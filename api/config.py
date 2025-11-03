import os


class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or "you_will_never_know"


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or "you_will_never_know"


def get_config():
    match os.getenv('ENV'):
        case 'PRODUCTION':
            return ProdConfig()
        case _:
            return DevConfig()
