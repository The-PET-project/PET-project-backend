import datetime
from functools import wraps
from flask import request
from flask_jwt_extended import decode_token, verify_jwt_in_request, create_access_token

from pet_project_backend.utils.jwt_payload import JwtPayload
from pet_project_backend.utils.error_handler import unauthorized_request_handler

MISSING_TOKEN = "A valid authentication token is missing! Add the 'Authorization' header with the value of: " \
                "'Bearer <JWT-TOKEN>' to every of your request."


def authenticate(func, admin_required=False):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        jwt = verify_jwt_in_request(request)
        if not jwt:
            return unauthorized_request_handler(MISSING_TOKEN)

        if 'Authorization' in request.headers:
            jwt_token = request.headers['Authorization'].removeprefix('Bearer ')


        decode_token(jwt_token)

        return func(*args, **kwargs)
    return decorated_function


def auth_builder(jwt_payload: JwtPayload):
    ONE_DAY = 86400  # in seconds

    jwt_payload = {
        'userId': jwt_payload.user.userId,
        'role': jwt_payload.role,
        'expiration': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    access_token = create_access_token(identity=jwt_payload,
                                       expires_delta=datetime.timedelta(days=1),
                                       fresh=True)
    return {
        'accessToken': access_token,
        'tokenType': 'Bearer',
        'expiresIn': ONE_DAY
    }