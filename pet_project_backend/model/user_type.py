from enum import Enum

from werkzeug.exceptions import BadRequest


class UserType(Enum):
    PET_OWNER = 'PET_OWNER',
    PET_CARER = 'PET_CARER'

    @staticmethod
    def list():
        return [i.name for i in UserType]

    @staticmethod
    def resolve(user_type: str):
        try:
            return UserType[user_type]
        except KeyError:
            raise BadRequest(f"The value of '{user_type}' is invalid for user-type. "
                             f"The valid values are: {UserType.list()}")
