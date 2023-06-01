from dataclasses import dataclass

from pet_project_backend.model import User
from pet_project_backend.model.user_role import UserRole


@dataclass
class JwtPayload:
    userId: str
    userName: str
    role: UserRole

    def __int__(self, user):
        self.userId = user.userId
        self.userName = user.username
        self.role = user.role
