from typing import Final
from typing import Union

from pet_project_backend.externals import db
from pet_project_backend.model.address import Address
from pet_project_backend.model.user_role import UserRole


class User(db.Model):
    __tablename__ = "user"

    userId = db.Column("user_id", db.Integer, autoincrement=True, primary_key=True)
    role = db.Column("role", db.Enum(UserRole), nullable=False)
    username = db.Column("username", db.String(100), nullable=False)
    email = db.Column("email", db.String(100), nullable=False)
    password = db.Column("password", db.String(100), nullable=False)
    firstName = db.Column("firstname", db.String(100), nullable=False)
    lastName = db.Column("lastname", db.String(100), nullable=False)
    middleName = db.Column("middlename", db.String(100))
    phone = db.Column("phone", db.String(30))
    mobile = db.Column("mobile", db.String(30))
    # DB relationships
    address = db.relationship("Address", uselist=False)

    LOGIN_FIELDS: Final = ["username", "password"]
    MINIMUM_REGISTRATION_FIELDS: Final = [
        "email",
        "username",
        "password",
        "firstName",
        "lastName",
    ]
    REGISTRATION_FIELDS: Final = [
        *MINIMUM_REGISTRATION_FIELDS,
        "middleName",
        "phone",
        "mobile",
        "address",
    ]
    ALL_FIELDS: Final = (["userId", "role", *REGISTRATION_FIELDS],)

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        firstName: str,
        lastName: str,
        middleName: str = "",
        userId: Union[int, None] = None,
        role: UserRole = UserRole.GUEST,
        phone: str = "",
        mobile: str = "",
        address: Union[dict, Address] = {},
    ):
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
            if isinstance(address, Address):
                self.address = Address
            else:
                # Filter out invalid fields.
                address_dict = {key: address.get(key) for key in Address.ALL_FIELDS}
                if all(key in address_dict for key in Address.CREATION_FIELDS):
                    self.address = Address(self.userId, **address_dict)  # type: ignore

    def __repr__(self):
        return (
            f"User(username={self.username}, email={self.email}, "
            f"firstName={self.firstName}, lastName={self.lastName})"
        )

    def to_dict(self):
        user_dict = {
            "userId": self.userId,
            "role": self.role.name,
            "username": self.username,
            "email": self.email,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "middleName": self.middleName,
            "phone": self.phone,
            "mobile": self.mobile,
        }
        if self.address:
            user_dict.update(self.address.to_dict())
        return user_dict

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.user_id == other.user_id

    def __ne__(self, other):
        return not self.__eq__(other)
