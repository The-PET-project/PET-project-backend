from flask_restx import fields

from pet_project_backend.externals import rest_api

"""Nested object in UserDTO/AccountDTO """
address_model = rest_api.model(
    "Address",
    {
        "address": fields.String(required=True, default="Main road 1"),
        "zipCode": fields.String(required=True, default="12345"),
        "city": fields.String(required=True, default="Miami"),
        "county": fields.String(required=True, default="Florida"),
        "country": fields.String(required=True, default="USA"),
    },
)

"""NOT A MODEL, but contains the basic public information about a User"""
__user_base_structure = {
    "username": fields.String(required=True, default="jDoe"),
    "email": fields.String(required=True, default="john.doe@mymail.com"),
    "firstName": fields.String(required=True, default="John"),
    "lastName": fields.String(required=True, default="Doe"),
    "middleName": fields.String(default="'TestUser'"),
    "phone": fields.String(default="+1-2345-6789"),
    "mobile": fields.String(default="+9-8765-4321"),
    "address": fields.Nested(address_model),
}

"""UserInputDTO describing the user details that entered by the User"""
user_input_model = rest_api.model(
    "UserInput",
    dict(
        {
            "password": fields.String(required=True, default="S3curePa55w0rd"),
            **__user_base_structure,
        }
    ),
)

"""UserDTO contains the user details"""
user_model = rest_api.model("User", dict({"userId": fields.Integer, **__user_base_structure}))

"""LoginInputDTO hold the credentials that entered by the User"""
login_input_model = rest_api.model(
    "LoginInput",
    {
        "username": fields.String(required=True, default="jDoe"),
        "password": fields.String(required=True, default="S3curePa55w0rd"),
    },
)

"""AuthDTO contains the authentication method for further requests"""
auth_model = rest_api.model(
    "Auth",
    {
        "accessToken": fields.String(required=True),
        "tokenType": fields.Integer(required=True),
        "expiresIn": fields.String(required=True),
    },
)

"""LoginDTO contains the user details and authentication info for further requests"""
login_model = rest_api.model(
    "Login",
    {
        "userDetails": fields.Nested(user_model),
        "authentication": fields.Nested(auth_model),
    },
)

"""ErrorMessageDTO describes the invalid client request, wrong user inputs, or the errors encountered in the system."""
error_message_model = rest_api.model(
    "ErrorMessage",
    {
        "errorMessage": fields.String(required=True, default="Some failure occurred."),
        "details": fields.String,
    },
)
