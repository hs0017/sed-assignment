from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    password = db.Column(db.Text)
    admin = db.Column(db.Boolean, default=False)


class Software_owner(db.Model):
    __tablename__ = 'software_owners'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    password = db.Column(db.Text)
    phone_extension = db.Column(db.Integer)


class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    phone = db.Column(db.Text)
    email = db.Column(db.Text)


class Software(db.Model):
    __tablename__ = 'software'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    version = db.Column(db.Text)
    license_expiry = db.Column(db.DateTime)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    vendor = db.relationship('Vendor', backref='software')
    academic_id = db.Column(db.Integer, db.ForeignKey('software_owners.id'))
    owner = db.relationship('Software_owner', backref='software')
