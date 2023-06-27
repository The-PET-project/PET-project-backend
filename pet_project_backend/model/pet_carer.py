from typing import Union

from sqlalchemy import Column
from sqlalchemy import Double
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from pet_project_backend.model import User
from pet_project_backend.model.user_role import UserRole


class PetCarer(User):
    __tablename__ = "pet_carer"

    petCarerId = Column("pet_carer_id", Integer, autoincrement=True, primary_key=True)
    userId = Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False)
    rating = Column("rating", Double)

    # DB relationships
    # routes = db.relationship('Route')

    def __init__(self, user: User, rating: Union[float, None], petCarerId: Union[int, None] = None):
        user_dict = user.to_dict()
        super().__init__(**user_dict, password=user.password)
        self.role = UserRole.USER
        self.__userId = user.userId
        self.__rating = rating
        self.__petCarerId = petCarerId

    def __repr__(self):
        return f"PetCarer(petCarerId={self.__petCarerId}, userId={self.__userId}, rating={self.__rating}"

    def to_dict(self):
        user_dict: dict = super().to_dict()
        user_dict.update({"petCarerId": self.__petCarerId, "rating": self.__rating})
        return user_dict

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.__petCarerId == other.__petCarerId
