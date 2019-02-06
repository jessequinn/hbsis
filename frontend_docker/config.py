import os


# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '\xd9w\xb5\xa1\x13\x82\xadC\xa2J\x81*e\xc6\x1c8\x8b\x92S3\r\x7fAl'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
