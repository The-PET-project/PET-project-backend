from json import JSONEncoder
from typing import Union

from sqlalchemy import Column
from sqlalchemy import Double
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from pet_project_backend.model import User
from pet_project_backend.model.user_role import UserRole


class PetOwner(User, JSONEncoder):
    __tablename__ = "pet_owner"

    ownerId = Column("owner_id", Integer, autoincrement=True, primary_key=True)
    userId = Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False)
    rating = Column("rating", Double)

    # DB relationships
    # petList = db.relationship('Pet')
    # usedServices = db.relationship('Service')

    def __init__(self, user: User, rating: Union[float, None], ownerId: Union[int, None] = None):
        user_dict = user.to_dict()
        super().__init__(**user_dict, password=user.password)
        self.role = UserRole.USER
        self.__userId = user.userId
        self.__rating = rating
        self.__ownerId = ownerId

    def __repr__(self):
        return f"PetOwner(ownerId={self.__ownerId}, userId={self.__userId}, rating={self.__rating}"

    def to_dict(self):
        user_dict: dict = super().to_dict()
        user_dict.update({"ownerId": self.__ownerId, "rating": self.__rating})
        return user_dict

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.__ownerId == other.__ownerId
