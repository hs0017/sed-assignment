from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

from . import db
from surreylm.database_models import Vendor, Software_owner, Software

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


# @views.route('/edit_software')
# @login_required
# def edit():
#     return render_template("edit_software.html", user=current_user)
#
# @views.route('/add_software')
# @login_required
# def add():
#     return render_template("add_software.html", user=current_user)

@views.route('/add_vendor', methods=['GET', 'POST'])
@login_required
def add_owner():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')

        vendor = Vendor.query.filter(func.lower(Vendor.name) == func.lower(name)).first()

        print(vendor)

        if vendor:
            flash('Manufacturer already exists.', category='error')
        elif len(name) < 4:
            flash('Manufacturer name must be greater than 3 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif not phone.isnumeric():
            flash('Phone number can only contain numeric characters.', category='error')
        else:
            new_vendor = Vendor(name=name, phone=phone, email=email)
            db.session.add(new_vendor)
            db.session.commit()
            flash('Manufacturer added!', category='success')
            return redirect(url_for('views.home'))

    return render_template("add_manufacturer.html", user=current_user)


@views.route('/add_owner', methods=['GET', 'POST'])
@login_required
def add_vendor():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_extension = request.form.get('phone_extension')

        owner = Software_owner.query.filter(func.lower(Software_owner.email) == func.lower(email)).first()

        if owner:
            flash('Software owner already exists.', category='error')
        elif not first_name.isalpha():
            flash('Owner name must not contain numbers', category='error')
        elif not last_name.isalpha():
            flash('Owner name must not contain numbers', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif not phone_extension.isnumeric():
            flash('Phone extension can only contain numeric characters.', category='error')
        elif len(phone_extension) != 4:
            flash('Phone extension must be 4 digits.', category='error')
        else:
            new_owner = Software_owner(email=email, first_name=first_name, last_name=last_name,
                                       phone_extension=phone_extension)
            db.session.add(new_owner)
            db.session.commit()
            flash('Owner added!', category='success')
            return redirect(url_for('views.home'))
    return render_template("add_owner.html", user=current_user)
