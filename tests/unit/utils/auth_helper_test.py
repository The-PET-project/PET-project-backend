import unittest
from datetime import datetime
from datetime import timedelta

from flask_restx import Api
from flask_restx import Namespace
from flask_restx import Resource

from pet_project_backend.app import create_app as create_application
from pet_project_backend.model.user_role import UserRole
from pet_project_backend.utils.helper import authenticate
from tests.unit.base_test_case import BaseTestCase

TEST_NAMESPACE = "unit-test"
TEST_ENDPOINT = "/test"
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403


class HelperTest(BaseTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_api = Api()
        test_api.add_namespace(test_ns)
        cls.app = create_application("pet_project_backend.config.TestConfiguration", api=test_api)

    def test_decorator_should_execute_the_decorated_function(self):
        valid_token = self.create_auth_token()
        headers = self.build_headers({"Authorization": f"Bearer {valid_token}"})

        response = self.client.get(f"/{TEST_NAMESPACE}{TEST_ENDPOINT}", headers=headers)
        assert response.status_code == HTTP_OK
        assert response.json["msg"] == "From decorated function."

    def test_decorator_should_return_401_Unauthorized_when_jwt_missing(self):
        headers = self.get_default_headers()

        response = self.client.get(f"/{TEST_NAMESPACE}{TEST_ENDPOINT}", headers=headers)
        assert response.status_code == HTTP_UNAUTHORIZED

    def test_decorator_should_return_400_if_a_jwt_data_field_is_missing(self):
        invalid_token = self.create_auth_token(user_id=None)
        headers = self.build_headers({"Authorization": f"Bearer {invalid_token}"})

        response = self.client.get(f"/{TEST_NAMESPACE}{TEST_ENDPOINT}", headers=headers)
        assert response.status_code == HTTP_BAD_REQUEST

    def test_decorator_should_return_403_Forbidden_if_user_role_is_not_admin_but_required(
        self,
    ):
        valid_token = self.create_auth_token()
        headers = self.build_headers({"Authorization": f"Bearer {valid_token}"})

        response = self.client.post(f"/{TEST_NAMESPACE}{TEST_ENDPOINT}", headers=headers)
        assert response.status_code == HTTP_FORBIDDEN

    def test_decorator_should_execute_the_decorated_function_with_admin_required_attr_when_the_user_is_admin(
        self,
    ):
        valid_token = self.create_auth_token(user_role=UserRole.ADMIN)
        headers = self.build_headers({"Authorization": f"Bearer {valid_token}"})

        response = self.client.post(f"/{TEST_NAMESPACE}{TEST_ENDPOINT}", headers=headers)
        assert response.status_code == HTTP_OK
        assert response.json["msg"] == "Only for admins."

    def test_decorator_should_NOT_execute_the_decorated_function_when_the_token_expired(
        self,
    ):
        expired_token = self.create_auth_token(time=datetime.now() - timedelta(hours=1))
        headers = self.build_headers({"Authorization": f"Bearer {expired_token}"})

        response = self.client.get(f"/{TEST_NAMESPACE}{TEST_ENDPOINT}", headers=headers)
        assert response.status_code == HTTP_UNAUTHORIZED


# =============== Test helpers ===============
test_ns = Namespace("unit-test")


@test_ns.route("/test")
class TestingClass(Resource):
    @authenticate(admin_required=False)
    def get(self, **kwargs):
        """Function that is created to be decorated for testing"""
        return {"msg": "From decorated function."}, 200

    @authenticate(admin_required=True)
    def post(self, **kwargs):
        """Function that is created to be decorated for testing"""
        return {"msg": "Only for admins."}, 200


if __name__ == "__main__":
    unittest.main()
