from flask_bcrypt import Bcrypt
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

"""REST Api"""
rest_api = Api(
    version="0.1.0",
    title="PET-project",
    license="MIT",
    prefix="/api/v1",
    contact="g4bor",
    contact_email="g4bor.dev@yahoo.com",
    summary="Pet-project - Hire a Pet Carer to have somebody to care about your pets when you are not at "
    "home, or be one of our pet sitters who enjoy working with animals. ",
    description="This is the backend API for the PET-project to manage the data of User, Pet, and PetCarer "
    "entities.",
)

"""SQLAlchemy instance"""
db = SQLAlchemy()

"""Bcrypt class container for password hashing and validating"""
bcrypt = Bcrypt()
