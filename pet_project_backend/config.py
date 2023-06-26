import os
from secrets import token_hex

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_db_uri():
    """Build database URI from environment variables"""
    DB_SCHEME = os.environ.get("DB_SCHEME", "mysql")
    DB_USERNAME = os.environ.get("DB_USERNAME", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_PORT = os.environ.get("DB_PORT", "3306")
    DB_DATABASE_SCHEMA = os.environ.get("DB_DATABASE_SCHEMA", "petproject")
    return f"{DB_SCHEME}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE_SCHEMA}"


class BaseConfiguration:
    env = os.environ.get("APP_ENV", "dev")
    load_dotenv(os.path.join(BASEDIR, "..", f".env.{env}"))
    DEBUG = False
    TESTING = False
    SECRET_KEY = token_hex(32)
    RESTX_MASK_SWAGGER = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    # Database
    SQLALCHEMY_DATABASE_URI = get_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class TestConfiguration(BaseConfiguration):
    load_dotenv(os.path.join(BASEDIR, "..", ".env.dev"))
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLITE_TEST_DB = os.path.join(BASEDIR, "..", "tests", "database.db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + SQLITE_TEST_DB
