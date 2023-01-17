import sys

from flask import Flask
from flask_restx import Api

from pet_project_backend.api import basic_controller


class Application:
    def __init__(self):
        self.__app = Flask(__name__)
        api = Api(
            self.__app,
            version="0.1",
            title="PET-project",
            description="Backend API for the PET-project to manage the data of User, Pet, and Walker entities.",
        )

        api.add_namespace(basic_controller)

    def get_app(self) -> Flask:
        return self.__app


if __name__ == "__main__":
    args = sys.argv
    application = Application().get_app()
    application.run(debug="debug" in args)
