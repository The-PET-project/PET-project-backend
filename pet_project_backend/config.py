import os
from secrets import token_hex


def get_db_uri():
    """Build database URI from environment variables"""
    DB_SCHEME = os.environ.get('DB_SCHEME', 'mysql')
    DB_USERNAME = os.environ.get('DB_USERNAME', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_DATABASE_SCHEMA = os.environ.get('DB_DATABASE_SCHEMA', 'petproject')
    return f'{DB_SCHEME}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE_SCHEMA}'


class BaseConfiguration(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = token_hex(32)
    SQLALCHEMY_DATABASE_URI = get_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    RESTX_MASK_SWAGGER = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')


class TestConfiguration(BaseConfiguration):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:?cache=shared'


