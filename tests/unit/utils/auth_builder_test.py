import pytest
from flask_jwt_extended import decode_token
from flask_restx import Api

from pet_project_backend.app import create_app
from pet_project_backend.config import TestConfiguration
from pet_project_backend.model import User
from pet_project_backend.model.user_role import UserRole
from pet_project_backend.utils.helper import auth_builder
from pet_project_backend.utils.helper import JWT_DATA_FIELDS

ONE_DAY = 86400


@pytest.fixture()
def app():
    app = create_app(TestConfiguration(), api=Api())
    return app


def test_auth_builder_create_proper_auth_response(app):
    test_user = User("testUser", "", "", "John", "QA", userId=1, role=UserRole.USER)

    with app.app_context():
        auth = auth_builder(test_user)

        jwt = decode_token(auth.get("accessToken"))
        assert auth.get("tokenType") == "Bearer"
        assert auth.get("expiresIn") == ONE_DAY
        assert isinstance(jwt, dict)
        assert "sub" in jwt  # Check for subject-claim in jwt-data


def test_created_jwt_token_contains_the_required_data(app):
    required_fields = JWT_DATA_FIELDS
    test_user = User("testUser", "", "", "John", "QA", userId=1, role=UserRole.USER)

    with app.app_context():
        auth = auth_builder(test_user)

        jwt = decode_token(auth.get("accessToken"))
        jwt_data = jwt.get("sub")
        assert all(field in jwt_data for field in required_fields)
        assert jwt_data.get("userId") == test_user.userId
        assert jwt_data.get("username") == test_user.username
        assert jwt_data.get("role") == test_user.role.name
