from pet_project_backend.database import db

ADDRESS_CREATION_FIELDS = ['address', 'zipCode', 'city', 'county', 'country']
ADDRESS_ALL_FIELDS = ['addressId', 'userId', *ADDRESS_CREATION_FIELDS]


class Address(db.Model):
    __tablename__ = "address"

    addressId = db.Column('address_id', db.Integer, autoincrement=True, primary_key=True)
    userId = db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    address = db.Column('address', db.String(100), nullable=False)
    zipCode = db.Column('zip_code', db.Integer, nullable=False)
    city = db.Column('city', db.String(100), nullable=False)
    county = db.Column('county', db.String(100), nullable=False)
    country = db.Column('country', db.String(100), nullable=False)

    def __init__(self, userId: int, address: str, zipCode: int, city: str, county: str, country: str,
                 addressId: int = None) -> None:
        super().__init__()
        self.userId = userId
        self.address = address
        self.zipCode = zipCode
        self.city = city
        self.county = county
        self.country = country
        self.addressId = addressId

    def __repr__(self):
        return f"Address(addressId={self.addressId}, userId={self.userId}, address={self.address}, " \
               f"zipCode={self.zipCode}, city={self.city}, county={self.county}, country={self.country})"

    def to_dict(self):
        return {
            "address": self.address,
            "zipCode": self.zipCode,
            "city": self.city,
            "county": self.county,
            "country": self.country
        }
