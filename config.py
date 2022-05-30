from ast import Pass
import os
from datetime import datetime, timedelta

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY= os.environ.get('SECRET_KEY')
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')


class DevolopmentCongig(Config):
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(BASE_DIR,'db.sqlite3')
    Pass

class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    pass

config = {
    'development': DevolopmentCongig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevolopmentCongig
}