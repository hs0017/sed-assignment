from flask import flash


class Validate:
    def __init__(self, password1, password2, first_name, last_name, email, entry, phone_number, phone_ext):
        self.password1 = password1
        self.password2 = password2
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.entry = entry
        self.phone_number = phone_number
        self.phone_ext = phone_ext

    @classmethod
    def password(cls, password1, password2, first_name, last_name):
        """
        This function is used to validate the password.
        :param password1: The first password.
        :param password2: The second password.
        :param first_name: The first name.
        :param last_name: The last name.
        :return: Returns True if the password is valid, else returns False.
        """
        password_valid = False
        if len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif str(password1).lower() == "password":
            flash('Password cannot be "password".', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif str(password1).lower() == str(first_name).lower() or str(password1).lower() == str(last_name).lower():
            flash('Password cannot be your first or last name.', category='error')
        else:
            password_valid = True
        return password_valid

    @classmethod
    def email(cls, email):
        """
        This function is used to validate the email.
        :param email: The email.
        :return: Returns True if the email is valid, else returns False.
        """
        email_valid = False
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        else:
            email_valid = True
        return email_valid

    @classmethod
    def people_name(cls, first_name, last_name):
        """
        This function is used to validate the first and last name.
        :param first_name: The first name.
        :param last_name: The last name.
        :return: Returns True if the first and last name are valid, else returns False.
        """
        people_name_valid = False
        if len(first_name) > 50 or len(first_name) < 1:
            flash('First name must be less than 50 characters and greater than 0', category='error')
        elif len(last_name) > 50 or len(last_name) < 1:
            flash('Last name must be less than 50 characters and greater than 0.', category='error')
        elif not first_name.isalpha() or not last_name.isalpha():
            flash('Names must only contain letters.', category='error')
        else:
            people_name_valid = True
        return people_name_valid

    @classmethod
    def generic_entry(cls, entry):
        """
        This function is used to validate the generic entry.
        :param entry: The entry.
        :return: Returns True if the entry is valid, else returns False.
        """
        generic_entry_valid = False
        if len(entry) < 1 or len(entry) > 50:
            flash('Entries must be greater than 1 character and less than 50.', category='error')
        else:
            generic_entry_valid = True
        return generic_entry_valid

    @classmethod
    def phone_number(cls, phone_number):
        """
        This function is used to validate the phone number.
        :param phone_number: The phone number.
        :return: Returns True if the phone number is valid, else returns False.
        """
        phone_number_valid = False
        if len(phone_number) != 11:
            flash('Phone number must be 11 digits.', category='error')
        elif not phone_number.isnumeric():
            flash('Phone number must only contain numbers.', category='error')
        else:
            phone_number_valid = True
        return phone_number_valid

    @classmethod
    def phone_ext(cls, phone_ext):
        """
        This function is used to validate the phone extension.
        :param phone_ext: The phone extension.
        :return: Returns True if the phone extension is valid, else returns False.
        """
        phone_ext_valid = False
        if len(phone_ext) != 4:
            flash('Phone extension must be 4 digits.', category='error')
        elif not phone_ext.isnumeric():
            flash('Phone extension must only contain numbers.', category='error')
        else:
            phone_ext_valid = True
        return phone_ext_valid
