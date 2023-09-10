"""Purpose of this file: This file contains the routes for adding, editing, viewing and deleting software, owners and
vendors. It also contains the functions that are used to validate user input."""

# Imports the required modules.
import datetime
from dateutil import relativedelta
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func, exc
from . import db
from surreylm.database_models import Vendor, Software_owner, Software
from surreylm.validations import Validate


views = Blueprint('views', __name__) # Creates a Blueprint object called 'views'.


@views.route('/')
@login_required
def home():
    """
    This function is used to render the home page.
    :return: Returns the home page, currently logged-in user, the current date, 1 month from the current date and all
     software records from the database.
    """
    software = Software.query.all()
    today = datetime.datetime.today()
    add_month = today + relativedelta.relativedelta(months=+1)
    return render_template("home.html", user=current_user, software=software, today=today,
                           add_month=add_month)


@views.route('/edit_software/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_software(id):
    """
    This function is used to edit software records.
    :param id: The id of the software record to be edited, passed from the home page.
    :return: The edit software page, currently logged-in user, the software record to be edited and all vendors and
    owners. The current vendor, owner and license expiry date are also passed to the page to be used in the form as
    the default pre-selected values.
    """
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

        software_name_valid = Validate.generic_entry(name)
        software_version_valid = Validate.generic_entry(version)

        if not software_name_valid or not software_version_valid:
            return render_template("edit_software.html", user=current_user, software=software,
                                   vendors=vendors, owners=owners, current_vendor=current_vendor,
                                   current_owner=current_owner, current_date=current_date,
                                   current_vendor_id=current_vendor_id, current_owner_id=current_owner_id)
        else:
            year, month, day = license_expiry.split('-')
            converted_date = datetime.date(int(year), int(month), int(day))
            software.name = name
            software.version = version
            software.license_expiry = converted_date
            software.vendor_id = vendor
            software.owner_id = owner
            db.session.commit()
            flash('Software updated!', category='success')
            return redirect(url_for('views.home'))
    return render_template("edit_software.html", user=current_user, software=software,
                           vendors=vendors, owners=owners, current_vendor=current_vendor, current_owner=current_owner,
                           current_date=current_date, current_vendor_id=current_vendor_id,
                           current_owner_id=current_owner_id)


@views.route('/add_vendor', methods=['GET', 'POST'])
@login_required
def add_vendor():
    """
    This function is used to add new vendors to the database.
    :return: Returns the add vendor page, currently logged-in user.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')

        vendor = Vendor.query.filter(func.lower(Vendor.name) == func.lower(name)).first()
        vendor_name_valid = Validate.generic_entry(name)
        vendor_phone_valid = Validate.phone_number(phone)
        vendor_email_valid = Validate.email(email)

        if vendor:
            flash('Vendor already exists.', category='error')
        elif not vendor_name_valid or not vendor_phone_valid or not vendor_email_valid:
            return render_template("add_manufacturer.html", user=current_user)
        else:
            new_vendor = Vendor(name=name, phone=phone, email=email)
            db.session.add(new_vendor)
            db.session.commit()
            flash('Vendor added!', category='success')
            return redirect(url_for('views.home'))

    return render_template("add_manufacturer.html", user=current_user)


@views.route('/add_owner', methods=['GET', 'POST'])
@login_required
def add_owner():
    """
    This function is used to add new owners to the database.
    :return: Returns the add owner page, currently logged-in user.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_extension = request.form.get('phone_extension')

        owner = Software_owner.query.filter(func.lower(Software_owner.email) == func.lower(email)).first()
        owner_name_valid = Validate.people_name(first_name, last_name)
        owner_email_valid = Validate.email(email)
        owner_phone_ext_valid = Validate.phone_ext(phone_extension)

        if owner:
            flash('Software owner already exists.', category='error')
        elif not owner_name_valid or not owner_email_valid or not owner_phone_ext_valid:
            return render_template("add_owner.html", user=current_user)
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
    """
    This function is used to add new software to the database.
    :return: Returns the add software page, currently logged-in user, all vendors and owner records from the database.
    """
    vendors = Vendor.query.all()
    owners = Software_owner.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        version = request.form.get('version')
        license_expiry = request.form.get('expiry_date')
        vendor = request.form.get('vendor')
        owner = request.form.get('owner')

        software_name_valid = Validate.generic_entry(name)
        software_version_valid = Validate.generic_entry(version)

        if not software_name_valid or not software_version_valid:
            return render_template("add_license.html", user=current_user, vendors=vendors, owners=owners)
        elif license_expiry == '':
            flash('Please enter a license expiry date.', category='error')
        elif vendor == 'Choose...':
            flash('Please select a vendor.', category='error')
        elif owner == 'Choose...':
            flash('Please select an owner.', category='error')
        else:
            year, month, day = license_expiry.split('-')
            converted_date = datetime.date(int(year), int(month), int(day))
            new_software = Software(name=name, version=version, license_expiry=converted_date, vendor_id=vendor,
                                    owner_id=owner)
            db.session.add(new_software)
            db.session.commit()
            flash('Software added!', category='success')
            return redirect(url_for('views.home'))
    return render_template("add_license.html", user=current_user, vendors=vendors, owners=owners)


@views.route('/delete_software/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_software(id):
    """
    This function is used to delete software records.
    :param id: The id of the software record to be deleted, passed from the home page.
    :return: Returns the home page.
    """
    software = Software.query.get_or_404(id)
    if current_user.admin:  # Checks if the current user is an admin.
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
    """
    This function is used to view owner records.
    :param id: The id of the owner record to be viewed, passed from the home page.
    :return: Returns the view owner page, currently logged-in user, the owner record to be viewed.
    """
    software = Software.query.filter_by(owner_id=id).all()
    owner = Software_owner.query.get_or_404(id)
    return render_template("view_owner.html", user=current_user, owner=owner, software=software)


@views.route('/view_vendor/<int:id>', methods=['GET', 'POST'])
@login_required
def view_vendor(id):
    """
    This function is used to view vendor records.
    :param id: The id of the vendor record to be viewed, passed from the home page.
    :return: Returns the view vendor page, currently logged-in user, the vendor record to be viewed.
    """
    software = Software.query.filter_by(vendor_id=id).all()
    vendor = Vendor.query.get_or_404(id)
    return render_template("view_vendor.html", user=current_user, vendor=vendor, software=software)


@views.route('/edit_owner/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_owner(id):
    """
    This function is used to edit owner records.
    :param id: The id of the owner record to be edited, passed from the view owner page.
    :return: Returns the edit owner page, currently logged-in user, the owner record to be edited.
    """
    owner = Software_owner.query.get_or_404(id)
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_extension = request.form.get('phone_extension')

        owner_name_valid = Validate.people_name(first_name, last_name)
        owner_email_valid = Validate.email(email)
        owner_phone_ext_valid = Validate.phone_ext(phone_extension)

        if not owner_name_valid or not owner_email_valid or not owner_phone_ext_valid:
            return render_template("edit_owner.html", user=current_user, owner=owner)

        owner.email = email
        owner.first_name = first_name
        owner.last_name = last_name
        owner.phone_extension = phone_extension
        db.session.commit()
        flash('Owner updated!', category='success')
        return redirect(url_for('views.view_owner', id=id))
    return render_template("edit_owner.html", user=current_user, owner=owner)


@views.route('/edit_vendor/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_vendor(id):
    """
    This function is used to edit vendor records.
    :param id: The id of the vendor record to be edited, passed from the view vendor page.
    :return: Returns the edit vendor page, currently logged-in user, the vendor record to be edited.
    """
    vendor = Vendor.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')

        vendor_name_valid = Validate.generic_entry(name)
        vendor_phone_valid = Validate.phone_number(phone)
        vendor_email_valid = Validate.email(email)

        if not vendor_name_valid or not vendor_phone_valid or not vendor_email_valid:
            return render_template("edit_vendor.html", user=current_user, vendor=vendor)

        vendor.name = name
        vendor.phone = phone
        vendor.email = email
        db.session.commit()
        flash('Manufacturer updated!', category='success')
        return redirect(url_for('views.view_vendor', id=id))
    return render_template("edit_vendor.html", user=current_user, vendor=vendor)


@views.route('/all_owners', methods=['GET', 'POST'])
@login_required
def all_owners():
    """
    This function is used to view all owner records.
    :return: Returns the all owners page, currently logged-in user, all owner records from the database.
    """
    owners = Software_owner.query.all()
    return render_template("all_owners.html", user=current_user, owners=owners)


@views.route('/delete_owner/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_owner(id):
    """
    This function is used to delete owner records.
    :param id: The id of the owner record to be deleted, passed from the all owners page.
    :return: Returns the all owners page.
    """
    owner = Software_owner.query.get_or_404(id)
    if current_user.admin:  # Checks if the current user is an admin.
        try:
            db.session.delete(owner)
            db.session.commit()
            flash('Owner deleted!', category='success')
            return redirect(url_for('views.all_owners'))
        except exc.IntegrityError:  # Handles the error if the owner is attached to existing software.
            flash('Owner cannot be deleted as they own existing software.', category='error')
            return redirect(url_for('views.all_owners'))
    else:
        flash('You do not have permission to delete owners.', category='error')
        return redirect(url_for('views.all_owners'))


@views.route('/all_vendors', methods=['GET', 'POST'])
@login_required
def all_vendors():
    """
    This function is used to view all vendor records.
    :return: Returns the all vendors page, currently logged-in user, all vendor records from the database.
    """
    vendors = Vendor.query.all()
    return render_template("all_vendors.html", user=current_user, vendors=vendors)


@views.route('/delete_vendor/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_vendor(id):
    """
    This function is used to delete vendor records.
    :param id: The id of the vendor record to be deleted, passed from the all vendors page.
    :return: Returns the all vendors page.
    """
    vendor = Vendor.query.get_or_404(id)
    if current_user.admin:  # Checks if the current user is an admin.
        try:
            db.session.delete(vendor)
            db.session.commit()
            flash('Vendor deleted!', category='success')
            return redirect(url_for('views.all_vendors'))
        except exc.IntegrityError:  # Handles the error if the vendor is attached to existing software.
            flash('Vendor cannot be deleted because it is attached to existing software.', category='error')
            return redirect(url_for('views.all_vendors'))
    else:
        flash('You do not have permission to delete manufacturers.', category='error')
        return redirect(url_for('views.all_vendors'))
