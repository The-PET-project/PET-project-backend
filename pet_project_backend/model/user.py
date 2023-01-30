from flask_restx import fields

from pet_project_backend.database import db


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.BIGINT, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    middlename = db.Column(db.String(100))
    phone = db.Column(db.String(30))
    mobile = db.Column(db.String(30))

    def __init__(self, username, email, password, firstname, lastname):
        self.username = username
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return f"User(username={self.username}, email={self.email}, firstname={self.firstname}, lastname={self.lastname})"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "middlename": self.middlename,
            "phone": self.phone,
            "mobile": self.mobile
        }

    def __eq__(self, other):
        return type(self) is type(other) and self.user_id == other.user_id

    def __ne__(self, other):
        return not self.__eq__(other)
