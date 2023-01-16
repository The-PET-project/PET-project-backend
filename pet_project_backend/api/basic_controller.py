import re

from flask_restx import Namespace, Resource, fields
from flask import make_response

RE_PATTERN = "[^a-zA-Z0-9]+"  # Regexp pattern to replace alpha-numeric characters


api = Namespace("/", "Basic operations")

user_model = api.model(
    "User",
    {
        "name": fields.String(
            required=True, description="The name of the user", example="John Doe"
        ),
        "email": fields.String(
            required=True,
            description="The email of the user",
            example="jdoe@mymail.com",
        ),
    },
)
example_user = {"name": "John Doe", "email": "jdoe@mymail.com"}


@api.route("/info")
class Info(Resource):
    @api.response(200, "Message")
    def get(self):
        return {
            "message": "Hello API user. You can find the API documentation on the root path: '<URL>/'"
        }, 200


@api.route("/info/<user>")
class UserInfo(Resource):
    @api.response(200, "Example User", user_model)
    def get(self):
        return make_response(example_user)


@api.route("/mock/user")
class MockUser(Resource):
    @api.response(200, "Mock User", user_model)
    def get(self):
        return example_user


@api.route("/mock/user/<string:name>")
@api.doc({"params": {"name": "The name of the mocked user."}})
class MockSelectedUser(Resource):
    @api.response(200, "Mock User", user_model)
    def get(self, name: str):
        email = re.sub(RE_PATTERN, "_", name.lower())
        mock_user = {"name": name, "email": f"{email}@mymail.com"}
        return mock_user
