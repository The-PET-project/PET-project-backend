from flask import jsonify
from flask_restx import Resource

from pet_project_backend.app import app, basic_space
from pet_project_backend.model import User


@basic_space.route("/")
class GetAllUsers(Resource):
    def get(self):
        """Get all users"""
        users = User.query.all()
        print(users)
        return jsonify([user.to_dict() for user in users])


@basic_space.route("/<int:user_id>")
class GetUserById(Resource):
    def get(self, user_id):
        """Get a user by id"""
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            return jsonify(user.to_dict())