import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:Hearty160@localhost/bucket_list'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

configuration = {
    'production': ProductionConfig,
    'staging': StagingConfig,
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': Config,
    'SECRET_KEY': os.environ["SECRET_KEY"]
}
