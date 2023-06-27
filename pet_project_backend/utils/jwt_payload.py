from dataclasses import dataclass

from pet_project_backend.model.user_role import UserRole


@dataclass
class JwtPayload:
    userId: str
    userName: str
    role: UserRole
    expiration: int

    def __int__(self, user_id: int, name: str, role: str, expiration: int):
        self.userId = str(user_id)
        self.userName = name
        self.role = UserRole.resolve(role)
        self.expiration = expiration
