import pytest
from unittest import TestCase
from flask import Flask
import json

from pet_project_backend.app import Application


class BasicControllerTest(TestCase):

    application: Flask = None

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.application = Application().get_app()

    def test_info_endpoint(self):
        response = self.application.test_client().get('/info')
        message = json.loads(response.data.decode('utf-8')).get("message")

        assert response.status_code == 200
        assert 'Hello API user' in message

    def test_example_user_endpoint(self):
        response = self.application.test_client().get('/mock/user')
        result = json.loads(response.data.decode('utf-8'))

        assert response.status_code == 200
        assert 'John Doe' == result.get('name')
        assert 'jdoe@mymail.com' == result.get('email')

    def test_mock_user_endpoint(self):
        expected_name = 'Jack The Tester'
        expected_email = 'jack_the_tester@mymail.com'

        response = self.application.test_client().get(f'/mock/user/{expected_name}')
        result = json.loads(response.data.decode('utf-8'))

        assert response.status_code == 200
        assert expected_name == result.get('name')
        assert expected_email == result.get('email')
