from pathlib import Path

DB_PATH = Path(__file__, '../db/users.db').resolve()
TEST_DB_PATH = Path(__file__, '../db/test_users.db').resolve()


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ddH32rtBx495'


class TestConfig:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{TEST_DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test'
