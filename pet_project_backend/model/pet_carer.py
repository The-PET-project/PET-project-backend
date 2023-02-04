from sqlalchemy import Column, Integer, ForeignKey, Double

from pet_project_backend.model import User


class PetCarer(User):
    __tablename__ = "pet_carer"

    petCarerId = Column('pet_carer_id', Integer, autoincrement=True, primary_key=True)
    userId = Column('user_id', Integer, ForeignKey('user.user_id'), nullable=False)
    rating = Column('rating', Double)

    # DB relationships
    # routes = db.relationship('Route')

    def __init__(self, user: User, rating: float = None, petCarerId: int = None):
        user_dict = user.to_dict()
        super().__init__(**user_dict, password=user.password)
        self.__userId = user
        self.__rating = rating
        self.__petCarerId = petCarerId

    def __repr__(self):
        return f"PetCarer(petCarerId={self.__petCarerId}, userId={self.__userId}, rating={self.__rating}"

    def to_dict(self):
        user_dict: dict = super(PetCarer, self).to_dict()
        user_dict.update({
            "petCarerId": self.__petCarerId,
            "rating": self.__rating
        })
        return user_dict