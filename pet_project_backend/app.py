import sys

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from pet_project_backend.api.auth_controller import auth_ns
from pet_project_backend.config import BaseConfiguration
from pet_project_backend.externals import db, rest_api, bcrypt


def create_app(config, api=rest_api):
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object(config)

    # Define API routes
    api.init_app(application)
    api.add_namespace(auth_ns)

    # Setup DB connection
    db.init_app(application)

    # Additional setup
    JWTManager(application)
    CORS(application)
    bcrypt.init_app(application)

    return application


if __name__ == "__main__":
    app = create_app(BaseConfiguration())
    app.run(host="0.0.0.0", port=5000, debug="debug" in sys.argv)
