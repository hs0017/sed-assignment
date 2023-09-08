# Purpose of this file: This file contains the database models for the License Management System.

# Importing the required modules.
from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    This class is used to create the User table in the database.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    admin = db.Column(db.Boolean, default=False)


class Software_owner(db.Model):
    """
    This class is used to create the Software_owner table in the database.
    """
    __tablename__ = 'software_owners'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    phone_extension = db.Column(db.Text, nullable=False)


class Vendor(db.Model):
    """
    This class is used to create the Vendor table in the database.
    """
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)


class Software(db.Model):
    """
    This class is used to create the Software table in the database.
    """
    __tablename__ = 'software'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    version = db.Column(db.Text, nullable=False)
    license_expiry = db.Column(db.DateTime, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    vendor = db.relationship('Vendor', backref='software')
    owner_id = db.Column(db.Integer, db.ForeignKey('software_owners.id'), nullable=False)
    owner = db.relationship('Software_owner', backref='software')
