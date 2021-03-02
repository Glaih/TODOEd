from os import environ
from pathlib import Path
from datetime import timedelta

DB_PATH = Path(__file__, '../db/users.db').resolve()
TEST_DB_PATH = Path(__file__, '../db/test_users.db').resolve()


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET')
    JWT_SECRET_KEY = environ.get('JWT_SECRET')
    JWT_TOKEN_LOCATION = ["json"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=2)
    DEBUG = False


class TestConfig:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{TEST_DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test'
    JWT_SECRET_KEY = 'test'
    JWT_TOKEN_LOCATION = ["json"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=60)
    DEBUG = True
