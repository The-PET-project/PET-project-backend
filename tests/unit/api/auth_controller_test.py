import unittest

from flask_restx import Api
from parameterized import parameterized

from pet_project_backend.api.auth_controller import auth_ns
from pet_project_backend.app import create_app as create_application
from pet_project_backend.externals import bcrypt
from pet_project_backend.model import PetCarer
from pet_project_backend.model import PetOwner
from pet_project_backend.model import User
from tests.unit.base_test_case import BaseTestCase

USER_DETAILS_FIELDS = [
    "userId",
    "role",
    "username",
    "email",
    "firstName",
    "lastName",
]


class AuthControllerTest(BaseTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_api = Api(prefix="/api/v1")
        test_api.add_namespace(auth_ns)
        cls.app = create_application("pet_project_backend.config.TestConfiguration", api=test_api)

    def test_registration_should_create_a_simple_account(self):
        # Given
        test_user: dict = self.create_test_user()
        # When
        response = self.client.post(
            "/api/v1/auth/registration",
            json=test_user,
            headers=self.get_default_headers(),
        )
        account = response.json
        # Then
        assert response.status_code == 201
        assert all(account[key] == test_user[key] for key in ["username", "email", "firstName", "lastName"])

    def test_registration_should_save_the_password_encrypted(self):
        # Given
        requested_username = "testUser"
        requested_password = "testUserPassword"
        test_user: dict = self.create_test_user(username=requested_username, password=requested_password)
        # When
        response = self.client.post(
            "/api/v1/auth/registration",
            json=test_user,
            headers=self.get_default_headers(),
        )
        # Then
        assert response.status_code == 201
        with self.app.app_context():
            saved_user: User = User.query.filter_by(username=requested_username).first()
            assert saved_user.password != requested_password
            assert bcrypt.check_password_hash(pw_hash=saved_user.password, password=requested_password)

    def test_registration_should_fail_if_a_required_field_is_missing(self):
        # Given
        test_user: dict = self.create_test_user()
        test_user.pop("firstName")
        # When
        response = self.client.post(
            "/api/v1/auth/registration",
            json=test_user,
            headers=self.get_default_headers(),
        )
        # Then
        assert response.status_code == 400
        assert all(key in response.json for key in ["errorMessage", "details"])

    def test_registration_should_fail_if_an_existing_email_was_given(self):
        # Given
        test_email = "john@mymail.com"
        self.save_user_into_db(username="johnTheFirst", email=test_email)
        test_user: dict = self.create_test_user(username="JohnDoe", email=test_email)
        # When
        response = self.client.post(
            "/api/v1/auth/registration",
            json=test_user,
            headers=self.get_default_headers(),
        )
        # Then
        assert response.status_code == 400
        assert all(key in response.json for key in ["errorMessage", "details"])

    def test_registration_should_fail_if_an_existing_username_was_given(self):
        # Given
        test_username = "johnDoe"
        self.save_user_into_db(username=test_username, email="johnny.the.first@mymail.com")
        test_user: dict = self.create_test_user(username=test_username, email="johnDoe@mymail.com")
        # When
        response = self.client.post(
            "/api/v1/auth/registration",
            json=test_user,
            headers=self.get_default_headers(),
        )
        # Then
        assert response.status_code == 400
        assert all(key in response.json for key in ["errorMessage", "details"])

    @parameterized.expand([("PET_OWNER", PetOwner), ("PET_CARER", PetCarer)])
    def test_registration_should_create_specific_type_of_user(self, user_type, account_type: PetOwner | PetCarer):
        assert self.app is not None
        # Given
        test_username = "testUser"
        test_user: dict = self.create_test_user(username=test_username)
        # When
        response = self.client.post(
            f"/api/v1/auth/registration/{user_type}",
            json=test_user,
            headers=self.get_default_headers(),
        )
        # Then
        assert response.status_code == 201
        with self.app.app_context():
            account = account_type.query.filter_by(username=test_username).first()
            assert isinstance(account, account_type)

    def test_registration_should_fail_if_the_specified_userType_was_invalid(
        self,
    ):
        # Given
        test_username = "testUser"
        test_user: dict = self.create_test_user(username=test_username)
        # When
        response = self.client.post(
            "/api/v1/auth/registration/SOME_INVALID_TYPE",
            json=test_user,
            headers=self.get_default_headers(),
        )
        # Then
        assert response.status_code == 400
        assert all(key in response.json for key in ["errorMessage", "details"])

    def test_successful_login_should_return_user_details_and_auth_token(self):
        # Given
        username, password = "testUser", "testUserPassword"
        self.save_user_into_db(username=username, password=password)
        credentials = {"username": username, "password": password}
        # When
        response = self.client.post(
            "/api/v1/auth/login",
            json=credentials,
            headers=self.get_default_headers(),
        )
        # Then
        assert response.status_code == 200
        assert all(key in response.json["userDetails"] for key in USER_DETAILS_FIELDS)
        assert all(key in response.json["authentication"] for key in ["accessToken", "tokenType", "expiresIn"])

    def test_login_should_fail_when_required_field_missing(self):
        # Given
        username, password = "testUser", "testUserPassword"
        self.save_user_into_db(username=username, password=password)
        invalid_credentials = {"password": password}
        # When
        response = self.client.post(
            "/api/v1/auth/login",
            json=invalid_credentials,
            headers=self.get_default_headers(),
        )
        # Then
        assert response.status_code == 400
        assert all(key in response.json for key in ["errorMessage", "details"])

    def test_login_should_fail_when_the_user_not_exist(self):
        # Given
        email, password = "testUser@mymail.com", "testUserPassword"
        self.save_user_into_db(username="someOtherUser")
        invalid_credentials = {"email": email, "password": password}
        # When
        response = self.client.post(
            "/api/v1/auth/login",
            json=invalid_credentials,
            headers=self.get_default_headers(),
        )
        # Then
        assert response.status_code == 400
        assert all(key in response.json for key in ["errorMessage", "details"])

    def test_login_should_fail_when_invalid_username_password_pair_is_given(
        self,
    ):
        # Given
        username, password = "testUser", "testUserPassword"
        self.save_user_into_db(username=username, password=password)
        credentials = {"username": username, "password": "wrongPassword"}
        # When
        response = self.client.post(
            "/api/v1/auth/login",
            json=credentials,
            headers=self.get_default_headers(),
        )
        # Then
        assert response.status_code == 401
        assert all(key in response.json for key in ["errorMessage", "details"])


if __name__ == "__main__":
    unittest.main()
