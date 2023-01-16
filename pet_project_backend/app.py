import sys

from flask import Flask
from flask_restx import Api

from pet_project_backend.api import basic_controller

app = Flask(__name__)
api = Api(
    app,
    version="0.1",
    title="PET-project",
    description="Backend API for the PET-project to manage the data of User, Pet, and Walker entities.",
)

api.add_namespace(basic_controller)

if __name__ == "__main__":
    args = sys.argv
    app.run(debug="debug" in args)
