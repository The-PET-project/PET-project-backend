from pet_project_backend.database import db
from pet_project_backend.model.address import ADDRESS_ALL_FIELDS, Address

USER_REQUIRED_LOGIN_FIELDS = ['username', 'password']
USER_REQUIRED_REGISTRATION_FIELDS = ['email', 'username', 'password', 'firstName', 'lastName']
USER_CREATION_FIELDS = [*USER_REQUIRED_REGISTRATION_FIELDS, 'middleName', 'phone', 'mobile', 'address']
USER_ALL_FIELDS = ['userId', *USER_CREATION_FIELDS]


class User(db.Model):
    __tablename__ = "user"

    userId = db.Column('user_id', db.Integer, autoincrement=True, primary_key=True)
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

    def __init__(self, username: str, email: str, password: str, firstName: str, lastName: str,
                 userId: int = None, middleName: str = None, phone: str = None, mobile: str = None,
                 address: dict = None):
        super().__init__()
        self.userId = userId
        self.username = username
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.middleName = middleName
        self.phone = phone
        self.mobile = mobile
        if address:
            address_dict = {key: address.get(key) for key in ADDRESS_ALL_FIELDS}  # Filter out invalid fields.
            self.address = Address(**address_dict)

    def __repr__(self):
        return f"User(username={self.username}, email={self.email}, " \
               f"firstName={self.firstName}, lastName={self.lastName})"

    def to_dict(self):
        address_dict = self.address.to_dict() if self.address else None
        return dict({
            "userId": self.userId,
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

