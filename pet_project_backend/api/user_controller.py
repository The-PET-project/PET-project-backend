import unittest
from typing import Final

from flask import jsonify
from flask_restx import Namespace
from flask_restx import Resource

from pet_project_backend.model import User
from pet_project_backend.utils.api_model import error_message_model
from pet_project_backend.utils.api_model import user_model
from pet_project_backend.utils.error_handler import http_404_resource_not_found_handler
from pet_project_backend.utils.helper import authenticate

# Constants
JSON_MIMETYPE: Final[str] = "application/json"
# Error message templates
INVALID_RESOURCE_ID: Final[str] = "There is no User with the given id: '%d'"


users_ns = Namespace("users")


@users_ns.route("/")
class GetAllUsers(Resource):
    @authenticate(admin_required=True)
    @users_ns.header("Authorization", 'Value: "Bearer <JWT-TOKEN>"')
    @users_ns.produces(JSON_MIMETYPE)
    @users_ns.response(200, "Success")
    @users_ns.marshal_list_with(user_model)
    def get(self, **kwargs):
        """Get all users"""
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200


@users_ns.route("/<int:user_id>")
class GetUserById(Resource):
    @authenticate(admin_required=True)
    @users_ns.header("Authorization", 'Value: "Bearer <JWT-TOKEN>"')
    @users_ns.produces(JSON_MIMETYPE)
    @users_ns.response(200, "Success", user_model)
    @users_ns.response(404, "Resource not found", error_message_model)
    def get(self, user_id, **kwargs):
        """Get a user by id"""
        user = User.query.filter_by(userId=user_id).first()
        if not user:
            return http_404_resource_not_found_handler(INVALID_RESOURCE_ID.format(user_id))

        return user.to_dict(), 200
