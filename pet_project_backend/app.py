import os
import sys

from flask import Flask
from flask_restx import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_jwt_extended import JWTManager

from pet_project_backend.config_parser import ConfigLoader
from pet_project_backend.database import db


def get_db_uri():
    """Build database URI from config values"""
    config = ConfigLoader.get_config()
    DB_SCHEME, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE_SCHEMA = config.values()
    return f'{DB_SCHEME}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE_SCHEMA}'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

engine = create_engine(get_db_uri())
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


rest_api = Api(app, version="0.1", title="PET-project", prefix='/api/v1',
               description="Backend API for the PET-project to manage the data of User, Pet, and Walker entities.",
               )

# Define server APIs
auth_space = rest_api.namespace('auth', description="CRUD operations related to registration & authentication")
basic_space = rest_api.namespace('users', description="Basic CRUD operations")

# Init the app when every adjustment is set
db.init_app(app)
jwt = JWTManager(app)
from pet_project_backend.api.basic_controller import *
from pet_project_backend.api.auth_controller import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug="debug" in sys.argv)
