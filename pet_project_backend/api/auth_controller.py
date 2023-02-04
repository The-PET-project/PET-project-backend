import datetime
from flask import request, make_response
from flask_restx import Resource
from flask_jwt_extended import create_access_token

from pet_project_backend.app import app, auth_space, db_session
from pet_project_backend.model import User, USER_REQUIRED_REGISTRATION_FIELDS, USER_REQUIRED_LOGIN_FIELDS, \
    USER_CREATION_FIELDS, ADDRESS_CREATION_FIELDS
from pet_project_backend.model.pet_carer import PetCarer
from pet_project_backend.model.pet_owner import PetOwner
from pet_project_backend.model.user_type import UserType
from pet_project_backend.utils.api_doc import create_api_doc_params, create_schema, create_schema_properties

address_props = create_schema_properties({
    'string': [i for i in ADDRESS_CREATION_FIELDS if i != 'zipCode'],
    'integer': ['zipCode']
})
address_schema = create_schema('object', address_props, ADDRESS_CREATION_FIELDS)

user_registration_props = create_schema_properties({
    'string': [i for i in USER_CREATION_FIELDS if i != 'address']
})
user_registration_props['address'] = address_schema
user_registration_model = create_schema('object', user_registration_props, USER_REQUIRED_REGISTRATION_FIELDS)


@auth_space.route("/registration")
class CreateNewBasicAccount(Resource):

    @auth_space.doc(summary="Registration",
                    description="This endpoint register a basic account and returns the result of the registration.",
                    params={ 'body': create_api_doc_params(
                        place_in='body', description='Send your user details for registration.',
                        schema=user_registration_model)})
    def post(self):
        """Create a new user with basic access"""
        data = request.get_json()
        validate_registration(user=data)
        user_dict = {key: data.get(key) for key in USER_CREATION_FIELDS}  # Filter out invalid fields.

        new_account = User(**user_dict)
        db_session.add(new_account)
        db_session.commit()

        res_body = {"message": "Registration was successful.", "userId": new_account.userId}
        return res_body, 201


@auth_space.route("/registration/<string:user_type>")
class CreateNewAccount(Resource):

    @auth_space.doc(summary="Registration",
                    description="This endpoint register a new account and returns the result of the registration.",
                    params={
                        'query': {'in': 'path', 'description': 'Define the user-type in path parameter'},
                        'body': create_api_doc_params(
                            place_in='body', description='Send your user details for registration.',
                            schema=user_registration_model)})
    def post(self, user_type):
        """Create a new user with the given type"""
        data = request.get_json()
        validate_registration(user=data)
        user_dict = {key: data.get(key) for key in USER_REQUIRED_REGISTRATION_FIELDS}  # Filter out invalid fields.

        basic_user = User(**user_dict)
        type_of_user = UserType[user_type]
        if type_of_user is UserType.PET_OWNER:
            new_account = PetOwner(basic_user)
        else:
            new_account = PetCarer(basic_user)
        db_session.add(new_account)
        db_session.commit()

        res_body = {"message": "Registration was successful.", "userId": new_account.userId}
        return res_body, 201


@auth_space.route("/login")
class Login(Resource):
    login_model = {field: {'type': 'string'} for field in USER_REQUIRED_LOGIN_FIELDS}
    login_schema = create_schema('object', login_model, USER_REQUIRED_LOGIN_FIELDS)

    @auth_space.doc(summary="Login", description="This endpoint returns the user data and a JWT authentication token.",
                    params={
                        'body': create_api_doc_params('body', 'Send your username and password', login_schema)
                    })
    def post(self):
        """Login a user"""
        data = request.get_json()
        user = User.query.filter_by(username=data["username"]).first()

        if user and user.password == data["password"]:
            access_token = create_jwt_token(userId=user.userId)
            body = {"user": user.to_dict(), "accessToken": access_token}
            return make_response(body, 200)
        else:
            return {"error": "The given username-password pair is invalid!"}, 401


def validate_registration(user):
    if not all([attr in user for attr in USER_REQUIRED_REGISTRATION_FIELDS]):
        raise ValueError(f'Missing required attribute. The following fields are required: '
                         f'{USER_REQUIRED_REGISTRATION_FIELDS}')

    existing_user = User.query.filter_by(username=user["username"]).first()
    if existing_user:
        return {"message": "The given username is already taken."}, 400

    existing_email = User.query.filter_by(email=user["email"]).first()
    if existing_email:
        return {"message": "The given email is already taken."}, 400


def create_jwt_token(userId):
    payload = {
        "userId": userId,
        "expiration": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return create_access_token(identity=payload, expires_delta=datetime.timedelta(days=1), fresh=True)
