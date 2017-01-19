import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:Hearty160@localhost/bucket_list'

class StagingConfig(Config):
    DEVELOPMENT = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

configuration = {
    'staging': StagingConfig,
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': Config,
    'SECRET_KEY': os.environ["SECRET_KEY"]
}
