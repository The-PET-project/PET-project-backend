from typing import Final

from pet_project_backend.externals import db
from pet_project_backend.model.address import Address
from pet_project_backend.model.user_role import UserRole


class User(db.Model):
    __tablename__ = "user"

    userId = db.Column('user_id', db.Integer, autoincrement=True, primary_key=True)
    role = db.Column('role', db.Enum(UserRole), nullable=False)
    username = db.Column('username', db.String(100), nullable=False)
    email = db.Column('email', db.String(100), nullable=False)
    password = db.Column('password', db.String(100), nullable=False)
    firstName = db.Column('firstname', db.String(100), nullable=False)
    lastName = db.Column('lastname', db.String(100), nullable=False)
    middleName = db.Column('middlename', db.String(100))
    phone = db.Column('phone', db.String(30))
    mobile = db.Column('mobile', db.String(30))
    # DB relationships
    address = db.relationship('Address', uselist=False)

    LOGIN_FIELDS: Final = ['username', 'password']
    MINIMUM_REGISTRATION_FIELDS: Final = ['email', 'username', 'password', 'firstName', 'lastName']
    REGISTRATION_FIELDS: Final = [*MINIMUM_REGISTRATION_FIELDS, 'middleName', 'phone', 'mobile', 'address']
    ALL_FIELDS: Final = ['userId', 'role', *REGISTRATION_FIELDS],

    def __init__(self, username: str, email: str, password: str, firstName: str, lastName: str, middleName: str = None,
                 userId: int = None, role: UserRole = UserRole.GUEST, phone: str = None, mobile: str = None,
                 address: dict = None):
        super().__init__()
        self.userId = userId
        self.role = role
        self.username = username
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.middleName = middleName
        self.phone = phone
        self.mobile = mobile
        if address:
            address_dict = {key: address.get(key) for key in Address.ALL_FIELDS}  # Filter out invalid fields.
            self.address = Address(**address_dict)

    def __repr__(self):
        return f"User(username={self.username}, email={self.email}, " \
               f"firstName={self.firstName}, lastName={self.lastName})"

    def to_dict(self):
        address_dict = self.address.to_dict() if self.address else None
        return dict({
            "userId": self.userId,
            "role": self.role,
            "username": self.username,
            "email": self.email,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "middleName": self.middleName,
            "phone": self.phone,
            "mobile": self.mobile,
            "address": address_dict
        })

    def __eq__(self, other):
        return type(self) is type(other) and self.user_id == other.user_id

    def __ne__(self, other):
        return not self.__eq__(other)
