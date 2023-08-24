from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from surreylm.database_models import Vendor

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

        vendor = Vendor.query.filter_by(name=name.lower()).first()

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
    return render_template("add_vendor.html", user=current_user)
