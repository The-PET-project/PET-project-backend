import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from pet_project_backend.api.auth_controller import auth_ns
from pet_project_backend.api.user_controller import users_ns
from pet_project_backend.externals import bcrypt
from pet_project_backend.externals import db
from pet_project_backend.externals import rest_api


def create_app(config, api=None):
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object(config)

    # Define API routes
    if not api:
        api = rest_api
        api.add_namespace(auth_ns)
        api.add_namespace(users_ns)
    api.init_app(application)

    # Setup DB
    db.init_app(application)

    # Additional setup
    JWTManager(application)
    CORS(application)
    bcrypt.init_app(application)

    return application


if __name__ == "__main__":
    app_config_name = os.environ.get("APP_CONFIG", "BaseConfiguration")
    app = create_app(f"pet_project_backend.config.{app_config_name}")
    app.run(host="0.0.0.0", port=5000, debug="debug" in sys.argv)
