import json
import unittest

from flask_restx import Api

from pet_project_backend.api.user_controller import users_ns
from pet_project_backend.app import create_app as create_application
from pet_project_backend.model.user_role import UserRole
from tests.unit.base_test_case import BaseTestCase


class UserControllerTest(BaseTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_api = Api(prefix="/api/v1")
        test_api.add_namespace(users_ns)
        cls.app = create_application('pet_project_backend.config.TestConfiguration', api=test_api)

    def test_get_all_users(self):
        # Given
        self.save_user_into_db("johnDoe", "jdoe@mymail.com", "password", UserRole.USER, "John", "Doe")
        self.save_user_into_db("testUser", "qa@mymail.com", "testUserPassword", UserRole.USER, "John", "QA")
        # When
        response = self.client.get("/api/v1/users/", headers=self.create_headers())
        result = json.loads(response.data.decode("utf-8"))
        # Then
        assert response.status_code == 200
        assert len(result) > 2

    def test_get_specific_user(self):
        # Given
        user_id, username, email = 1, "testUser", "qa@mymail.com"
        # test_user = User(username, email, 'testUserPassword', 'John', 'QA', userId=user_id)
        self.save_user_into_db(username, email, "testUserPassword", firstName="John", lastName="QA", userId=user_id)
        # When
        response = self.client.get(f"/api/v1/users/{user_id}", headers=self.create_headers())
        result = json.loads(response.data.decode("utf-8"))
        # Then
        assert response.status_code == 200
        assert result.get("username") == username
        assert result.get("email") == email

    def test_user_not_found(self):
        # Given
        user_id, username, email = 1, "testUser", "qa@mymail.com"
        self.save_user_into_db(username, email, "testUserPassword", firstName="John", lastName="QA", userId=user_id)
        # When
        response = self.client.get("/api/v1/users/123", headers=self.create_headers())
        # Then
        assert response.status_code == 404
        assert all(key in response.json for key in ["errorMessage", "details"])

    # ===== Helper functions =====
    def create_headers(self):
        valid_token = self.create_auth_token(user_role=UserRole.ADMIN)
        headers = self.get_default_headers()
        headers["Authorization"] = f"Bearer {valid_token}"
        return headers


if __name__ == '__main__':
    unittest.main()
