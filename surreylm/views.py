import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

from . import db
from surreylm.database_models import Vendor, Software_owner, Software

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    software = Software.query.all()
    return render_template("home.html", user=current_user, software=software)


@views.route('/edit_software/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_software(id):
    software = Software.query.get_or_404(id)
    current_vendor = software.vendor.name
    current_vendor_id = software.vendor.id
    current_date = software.license_expiry.strftime('%Y-%m-%d')
    vendors = Vendor.query.all()
    owners = Software_owner.query.all()
    current_owner = software.owner.first_name + ' ' + software.owner.last_name
    current_owner_id = software.owner.id
    if request.method == 'POST':
        name = request.form.get('name')
        version = request.form.get('version')
        license_expiry = request.form.get('expiry_date')
        vendor = request.form.get('vendor')
        owner = request.form.get('owner')
        year, month, day = license_expiry.split('-')
        converted_date = datetime.date(int(year), int(month), int(day))

        if len(name) < 1:
            flash('Software name must be greater than 0 characters.', category='error')
        elif len(version) < 1:
            flash('Software version must be greater than 0 characters.', category='error')
        else:
            software.name = name
            software.version = version
            software.license_expiry = converted_date
            software.vendor_id = vendor
            software.academic_id = owner
            db.session.commit()
            flash('Software updated!', category='success')
            return redirect(url_for('views.home'))
    return render_template("edit_software.html", user=current_user, software=software, vendors=vendors, owners=owners,
                           current_vendor=current_vendor, current_owner=current_owner, current_date=current_date, current_vendor_id=current_vendor_id, current_owner_id=current_owner_id)


@views.route('/add_vendor', methods=['GET', 'POST'])
@login_required
def add_vendor():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')

        vendor = Vendor.query.filter(func.lower(Vendor.name) == func.lower(name)).first()

        if vendor:
            flash('Manufacturer already exists.', category='error')
        elif len(name) < 4:
            flash('Manufacturer name must be greater than 3 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif not phone.isnumeric():
            flash('Phone number can only contain numeric characters.', category='error')
        elif len(phone) != 11:
            flash('Phone number must be 11 digits.', category='error')
        else:
            new_vendor = Vendor(name=name, phone=phone, email=email)
            db.session.add(new_vendor)
            db.session.commit()
            flash('Manufacturer added!', category='success')
            return redirect(url_for('views.home'))

    return render_template("add_manufacturer.html", user=current_user)


@views.route('/add_owner', methods=['GET', 'POST'])
@login_required
def add_owner():
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


@views.route('/add_software', methods=['GET', 'POST'])
@login_required
def add_software():
    vendors = Vendor.query.all()
    owners = Software_owner.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        version = request.form.get('version')
        license_expiry = request.form.get('expiry_date')
        vendor = request.form.get('vendor')
        owner = request.form.get('owner')
        year, month, day = license_expiry.split('-')
        converted_date = datetime.date(int(year), int(month), int(day))

        software = Software.query.filter(func.lower(Software.name) == func.lower(name)).first()

        if software:
            flash('Software already exists.', category='error')
        elif len(name) < 1:
            flash('Software name must be greater than 0 characters.', category='error')
        elif len(version) < 1:
            flash('Software version must be greater than 0 characters.', category='error')
        else:
            new_software = Software(name=name, version=version, license_expiry=converted_date, vendor_id=vendor,
                                    academic_id=owner)
            db.session.add(new_software)
            db.session.commit()
            flash('Software added!', category='success')
            return redirect(url_for('views.home'))
    return render_template("add_license.html", user=current_user, vendors=vendors, owners=owners)


@views.route('/delete_software/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_software(id):
    software = Software.query.get_or_404(id)
    if current_user.admin:
        db.session.delete(software)
        db.session.commit()
        flash('Software deleted!', category='success')
        return redirect(url_for('views.home'))
    else:
        flash('You do not have permission to delete software.', category='error')
        return redirect(url_for('views.home'))


@views.route('/view_owner/<int:id>', methods=['GET', 'POST'])
@login_required
def view_owner(id):
    software = Software.query.filter_by(academic_id=id).all()
    owner = Software_owner.query.get_or_404(id)
    return render_template("view_owner.html", user=current_user, owner=owner, software=software)

@views.route('/view_vendor/<int:id>', methods=['GET', 'POST'])
@login_required
def view_vendor(id):
    software = Software.query.filter_by(vendor_id=id).all()
    vendor = Vendor.query.get_or_404(id)
    return render_template("view_vendor.html", user=current_user, vendor=vendor, software=software)

