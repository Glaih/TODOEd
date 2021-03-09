from os import environ
from datetime import timedelta


DB_PASSWORD = environ['DB_PASSWORD']
DB_LOGIN = environ['DB_LOGIN']
DB_HOST = environ['DB_HOST']
DB_NAME = 'todo'
TEST_DB_NAME = 'test_todo'


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ['SECRET']
    JWT_SECRET_KEY = environ['JWT_SECRET']
    JWT_TOKEN_LOCATION = ["json"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=2)
    DEBUG = False


class TestConfig:
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}/{TEST_DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test'
    JWT_SECRET_KEY = 'test'
    JWT_TOKEN_LOCATION = ["json"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=60)
    DEBUG = True
