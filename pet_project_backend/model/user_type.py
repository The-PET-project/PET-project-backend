from enum import Enum


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
            return None
