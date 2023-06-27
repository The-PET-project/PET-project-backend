from datetime import datetime
from datetime import timedelta
from functools import wraps

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import verify_jwt_in_request

from pet_project_backend.model import User
from pet_project_backend.model.user_role import UserRole
from pet_project_backend.utils.error_handler import (
    http_400_bad_request_handler,
)
from pet_project_backend.utils.error_handler import (
    http_401_unauthorized_request_handler,
)
from pet_project_backend.utils.error_handler import (
    http_403_forbidden_request_handler,
)

MISSING_TOKEN = (
    "A valid authentication token is missing! Add the 'Authorization' header with the value of: "
    "'Bearer <JWT-TOKEN>' to every of your request."
)
EXPIRED_TOKEN = "The provided JWT token is expired. Please, login to get a valid token."
INVALID_JWT = "The provided JWT token is invalid or corrupted. Please, re-login to have a valid token."
ADMIN_CONTENT = "The desired resource is accessible only with ADMIN rights."

JWT_DATA_FIELDS = ["userId", "username", "role", "expiration"]


def authenticate(admin_required=False):
    """API decorator that add JWT token check functionality to the decorated function"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Verify JWT token exist in the request
            jwt = verify_jwt_in_request(optional=False)
            if not jwt:
                return http_401_unauthorized_request_handler(MISSING_TOKEN)
            jwt_data = get_jwt_identity()
            # Check JWT token validity
            if not all(field in jwt_data for field in JWT_DATA_FIELDS):
                return http_400_bad_request_handler(INVALID_JWT)
            # Verify JWT expiration date
            if datetime.fromisoformat(jwt_data.get("expiration")) < datetime.now():
                return http_401_unauthorized_request_handler(EXPIRED_TOKEN)
            # Authorization check
            user_role = UserRole.resolve(jwt_data["role"])
            if admin_required and user_role != UserRole.ADMIN:
                return http_403_forbidden_request_handler(ADMIN_CONTENT)

            # jwt_user = User.query.filter_by(username=jwt_data['username']).first()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def auth_builder(user: User):
    """Helper function that creates and wraps into a dict the authentication details for a given user"""
    ONE_DAY = 86400  # in seconds

    expiration = datetime.now() + timedelta(days=1)
    jwt_data = {
        "userId": user.userId,
        "username": user.username,
        "role": user.role.name,
        "expiration": expiration.isoformat(timespec="seconds"),
    }
    access_token = create_access_token(identity=jwt_data, expires_delta=timedelta(days=1), fresh=True)
    return {
        "accessToken": access_token,
        "tokenType": "Bearer",
        "expiresIn": ONE_DAY,
    }
