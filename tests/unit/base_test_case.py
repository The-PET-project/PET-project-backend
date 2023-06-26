from datetime import datetime
from datetime import timedelta
from unittest import TestCase

from flask_jwt_extended import create_access_token

from pet_project_backend.app import create_app as create_application
from pet_project_backend.externals import bcrypt
from pet_project_backend.externals import db
from pet_project_backend.model import User
from pet_project_backend.model.user_role import UserRole


class BaseTestCase(TestCase):
    """A base test case for flask application testing."""

    app = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_application('pet_project_backend.config.TestConfiguration')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.app = None

    def setUp(self) -> None:
        assert self.app is not None
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self) -> None:
        assert self.app is not None
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        del self.client

    def create_auth_token(
        self,
        user_id: int = 1,
        username: str = "testUser",
        user_role: UserRole = UserRole.USER,
        time: datetime = datetime.now(),
    ):
        delta = timedelta(minutes=1)
        expiration_time = time + delta
        jwt_data = {
            "userId": user_id,
            "username": username,
            "role": user_role.name,
            "expiration": expiration_time.isoformat(timespec="seconds"),
        }
        cleaned_jwt_data = {key: value for key, value in jwt_data.items() if value is not None}

        assert self.app is not None
        with self.app.app_context():
            auth_token = create_access_token(identity=cleaned_jwt_data, expires_delta=delta)
        return auth_token

    def save_user_into_db(
        self,
        username="testUser",
        email="qa@mymail.com",
        password="pass",
        role=UserRole.USER,
        firstName="John",
        lastName="QA",
        **kwargs,
    ):
        encrypted_password = bcrypt.generate_password_hash(password)
        user_to_save = User(username, email, encrypted_password, firstName, lastName, role=role, **kwargs)
        with self.app.app_context():
            db.session.add(user_to_save)
            db.session.commit()

    @staticmethod
    def get_default_headers():
        return {"accept": "application/json", "Content-Type": "application/json"}

    @staticmethod
    def build_headers(additional_headers: dict):
        headers = BaseTestCase.get_default_headers()
        headers.update(additional_headers)
        return headers

    @staticmethod
    def create_test_user(
        username="testUser", email="qa@mymail.com", password="pass", firstName="John", lastName="QA"
    ) -> dict:
        return {
            "username": username,
            "email": email,
            "password": password,
            "firstName": firstName,
            "lastName": lastName,
        }
