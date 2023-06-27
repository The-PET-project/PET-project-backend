from __future__ import annotations

from typing import Final

from flask import request
from flask_restx import Namespace
from flask_restx import Resource
from werkzeug.exceptions import BadRequest

from pet_project_backend.externals import bcrypt
from pet_project_backend.externals import db
from pet_project_backend.model import PetCarer
from pet_project_backend.model import PetOwner
from pet_project_backend.model import User
from pet_project_backend.model.user_type import UserType
from pet_project_backend.utils.api_model import error_message_model
from pet_project_backend.utils.api_model import login_input_model
from pet_project_backend.utils.api_model import login_model
from pet_project_backend.utils.api_model import user_input_model
from pet_project_backend.utils.api_model import user_model
from pet_project_backend.utils.error_handler import (
    http_400_bad_request_handler,
)
from pet_project_backend.utils.error_handler import (
    http_401_unauthorized_request_handler,
)
from pet_project_backend.utils.helper import auth_builder

# Constants
JSON_MIMETYPE: Final[str] = "application/json"
# Error message templates
MISSING_ATTRIBUTE: Final[str] = "Missing required attribute. The following fields are required: %s!"
INVALID_USER_TYPE: Final[str] = f'The given user-type is invalid. The possible values are: {", ".join(UserType.list())}'
WRONG_CREDENTIALS: Final[str] = "The given username-password pair is invalid!"
INVALID_LOGIN_FORM: Final[str] = "The fields: 'username' and 'password' are mandatory."


auth_ns = Namespace("auth")


@auth_ns.route("/registration")
class CreateNewBasicAccount(Resource):
    @auth_ns.expect(user_input_model)
    @auth_ns.produces(JSON_MIMETYPE)
    @auth_ns.response(201, "Created", user_model)
    @auth_ns.response(400, "Bad request", error_message_model)
    @auth_ns.response(409, "Conflict", error_message_model)
    @auth_ns.doc(
        summary="Registration",
        description="Register a basic account and returns the user details.",
    )
    def post(self):
        """Create a new user with basic access"""
        user_data = request.get_json()
        try:
            validate_registration(user=user_data)
        except BadRequest as error:
            return http_400_bad_request_handler(error.description)

        user_data["password"] = bcrypt.generate_password_hash(user_data["password"])
        # Filter out invalid fields.
        user_dict = {key: user_data.get(key) for key in User.REGISTRATION_FIELDS}

        new_account = User(**user_dict)
        db.session.add(new_account)
        db.session.commit()
        return new_account.to_dict(), 201


@auth_ns.route("/registration/<string:user_type>")
class CreateNewAccount(Resource):
    @auth_ns.expect(user_input_model)
    @auth_ns.produces(JSON_MIMETYPE)
    @auth_ns.response(201, "Created", user_model)
    @auth_ns.response(400, "Bad request", error_message_model)
    @auth_ns.response(409, "Conflict", error_message_model)
    @auth_ns.doc(
        summary="Registration",
        description="Register an account with a specific role and returns the user details.",
    )
    def post(self, user_type):
        """Create a new user with the given user-type"""
        user_data = request.get_json()
        try:
            validate_registration(user=user_data)
        except BadRequest as error:
            return http_400_bad_request_handler(error.description)

        type_of_user = UserType.resolve(user_type)
        if not type_of_user:
            return http_400_bad_request_handler(INVALID_USER_TYPE)

        user_data["password"] = bcrypt.generate_password_hash(user_data["password"])
        # Filter out invalid fields.
        user_dict = {key: user_data.get(key) for key in User.REGISTRATION_FIELDS}

        basic_user = User(**user_dict)
        if type_of_user is UserType.PET_OWNER:
            new_account = PetOwner(basic_user, 0.0)
        elif type_of_user is UserType.PET_CARER:
            new_account = PetCarer(basic_user, 0.0)
        else:
            return http_400_bad_request_handler(INVALID_USER_TYPE)

        db.session.add(new_account)
        db.session.commit()
        return new_account.to_dict(), 201


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_input_model)
    @auth_ns.produces(JSON_MIMETYPE)
    @auth_ns.response(200, "Success", login_model)
    @auth_ns.response(400, "Bad request", error_message_model)
    @auth_ns.response(401, "Unauthorized", error_message_model)
    @auth_ns.doc(
        summary="Login",
        description="Authenticate the user and if it is successful then"
        "return the user details and JWT authentication token.",
    )
    def post(self):
        """Login a user"""
        credentials = request.get_json()

        if not all(key in credentials for key in User.LOGIN_FIELDS):
            return http_400_bad_request_handler(INVALID_LOGIN_FORM)

        user = User.query.filter_by(username=credentials["username"]).first()
        if not user:
            return http_401_unauthorized_request_handler(WRONG_CREDENTIALS)
        if not is_valid_password(credentials["password"], user):
            return http_401_unauthorized_request_handler(WRONG_CREDENTIALS)

        body = {
            "userDetails": user.to_dict(),
            "authentication": auth_builder(user),
        }

        return body, 200


def validate_registration(user):
    if not all([attr in user for attr in User.MINIMUM_REGISTRATION_FIELDS]):
        raise BadRequest(MISSING_ATTRIBUTE.format(User.MINIMUM_REGISTRATION_FIELDS))

    existing_user = User.query.filter_by(username=user["username"]).first()
    if existing_user:
        raise BadRequest("The given username is already taken.")

    existing_email = User.query.filter_by(email=user["email"]).first()
    if existing_email:
        raise BadRequest("The given email is already registered.")


def is_valid_password(password, user):
    return bcrypt.check_password_hash(pw_hash=user.password, password=password)
