import configparser
import sys

from flask import Flask
from flask_restx import Api

from pet_project_backend.database import db


def get_db_URI():
    """Build database URI from config values"""
    config = configparser.ConfigParser()
    config.read('../config/config.ini')
    db_conf = {key: value for (key, value) in config['MYSQL-DB'].items()}
    username, password, host, port, database_name = db_conf.values()
    return f'mysql://{username}:{password}@{host}:{port}/{database_name}'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_URI()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APIs = {}

rest_api = Api(
    app,
    version="0.1",
    title="PET-project",
    prefix='/api/v1',
    description="Backend API for the PET-project to manage the data of User, Pet, and Walker entities.",
)

# Define server APIs
basic_space = rest_api.namespace('users', description="Basic CRUD operations")

# Init the app when every adjustment is set
db.init_app(app)
from pet_project_backend.api.basic_controller import *


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug="debug" in sys.argv)
