from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    password = db.Column(db.Text)
    admin = db.Column(db.Boolean, default=False)


class Academic(db.Model):
    __tablename__ = 'academics'
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
    academic_id = db.Column(db.Integer, db.ForeignKey('academics.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

