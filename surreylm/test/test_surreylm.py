import pytest
from werkzeug.security import generate_password_hash
from surreylm import create_app
from surreylm import db
from surreylm.database_models import User, Software_owner, Vendor, Software



@pytest.fixture()
def app():
    app = create_app()  # Creating the flask app with an in-memory database.
    with app.app_context():
        db.create_all()
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_request_example(client):
    response = client.get("/", follow_redirects=True)
    assert len(response.history) == 1
    assert response.request.path == "/login"


def test_login(client):
    response = client.get("/login", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_post_invalid(client):
    response = client.post("/login", data={"email": "amylang@gmail.com", "password": "Pandabear55"},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b"Incorrect login details, please try again or contact your system administrator." in response.data
    assert response.request.path == "/login"


def test_register(client):
    response = client.get("/register", follow_redirects=True)
    assert response.status_code == 200
    assert b"Register" in response.data


def test_register_post(app, client):
    response = client.post("/register", data={"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@outlook.com",
                                              "password1": "Pandabear55", "password2": "Pandabear55"},
                           follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "jane.doe@outlook.com"
    assert b"Home" in response.data
    assert response.request.path == "/"
    assert b"Account created!" in response.data


def test_register_post_invalid(client):
    response = client.post("/register", data={"first_name": "Henry", "last_name": "Watson", "email": "c@",
                                              "password1": "Pandabear55", "password2": "Pandabear55"},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b"Email must be greater than 3 characters." in response.data
    assert response.request.path == "/register"


def test_login_post(client):
    client.post("/register", data={"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@outlook.com",
                                   "password1": "Pandabear55", "password2": "Pandabear55"}, follow_redirects=True)
    response = client.post("/login", data={"email": "jane.doe@outlook.com", "password": "Pandabear55"},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b"Home" in response.data
    assert response.request.path == "/"


def register(client):
    return client.post("/register", data={"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@outlook.com",
                                          "password1": "Pandabear55", "password2": "Pandabear55"},
                       follow_redirects=True)


def login(client):
    return client.post("/login", data={"email": "jane.doe@outlook.com", "password": "Pandabear55"},
                       follow_redirects=True)


def test_add_vendor(client, app):
    register(client)
    login(client)
    response = client.post("/add_vendor",
                           data={"name": "Mathworks", "email": "support@mathworks.com", "phone": "09876827994"},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b"Vendor added!" in response.data
    with app.app_context():
        assert Vendor.query.count() == 1
        assert Vendor.query.first().name == "Mathworks"
    assert response.request.path == "/"


def test_add_vendor_invalid(client, app):
    register(client)
    login(client)
    response = client.post("/add_vendor",
                           data={"name": "Mathworks", "email": "support@mathworks.com'", "phone": "098768"},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b"Phone number must be 11 digits." in response.data
    with app.app_context():
        assert Vendor.query.count() == 0    # The vendor should not have been added.
    assert response.request.path == "/add_vendor"


def test_add_software_owner(client, app):
    register(client)
    login(client)
    response = client.post("/add_owner",
                           data={"first_name": "John", "last_name": "Power", "email": "j.power@hotmail.co.uk",
                                 "phone_extension": "1234"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Owner added!" in response.data
    with app.app_context():
        assert Software_owner.query.count() == 1
        assert Software_owner.query.first().email == "j.power@hotmail.co.uk"
    assert response.request.path == "/"


def test_add_software_owner_invalid(client, app):
    register(client)
    login(client)
    response = client.post("/add_owner",
                           data={"first_name": "John", "last_name": "Power1", "email": "john.power@hotmail.co.uk",
                                 "phone_extension": "1234"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Names must only contain letters." in response.data
    with app.app_context():
        assert Software_owner.query.count() == 0    # The owner should not have been added.
    assert response.request.path == "/add_owner"


def add_vendor(client):
    return client.post("/add_vendor",
                       data={"name": "Mathworks", "email": "support@mathworks.com", "phone": "09876827994"},
                       follow_redirects=True)


def add_owner(client):
    return client.post("/add_owner",
                       data={"first_name": "John", "last_name": "Power", "email": "johnp@gmail.co.uk",
                             "phone_extension": "1234"}, follow_redirects=True)


def test_add_sofware(client, app):
    register(client)
    login(client)
    add_vendor(client)
    add_owner(client)
    response = client.post("/add_software",
                           data={"name": "MATLAB", "version": "R2020b", "expiry_date": "2024-12-31",
                                 "vendor": "1", "owner": "1"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Software added!" in response.data
    with app.app_context():
        software = Software.query.get_or_404(1)
        assert Software.query.count() == 1
        assert Software.query.first().name == "MATLAB"
        assert software.owner.first_name == "John"  # The owner should be John.
    assert response.request.path == "/"


def test_add_software_invalid(client, app):
    register(client)
    login(client)
    add_vendor(client)
    add_owner(client)
    response = client.post("/add_software",
                           data={"name": "MATLAB", "version": "",
                                 "expiry_date": "2024-12-31",
                                 "vendor": "1", "owner": "1"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Entries must be greater than 1 character and less than 50." in response.data
    with app.app_context():
        assert Software.query.count() == 0  # The software should not have been added.
    assert response.request.path == "/add_software"


def add_software(client):
    return client.post("/add_software",
                       data={"name": "MATLAB", "version": "R2020b", "expiry_date": "2024-12-31",
                             "vendor": "1", "owner": "1"}, follow_redirects=True)


def test_edit_vendor(client, app):
    register(client)
    login(client)
    add_vendor(client)
    response = client.post("/edit_vendor/1",
                           data={"name": "Mathworks", "email": "mathworks_support@mathworks.com",
                                 "phone": "09876827994"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Vendor updated!" in response.data
    with app.app_context():
        assert Vendor.query.count() == 1
        assert Vendor.query.first().email == "mathworks_support@mathworks.com"  # The email should have changed.
    assert response.request.path == "/view_vendor/1"


def test_edit_vendor_invalid(client, app):
    register(client)
    login(client)
    add_vendor(client)
    response = client.post("/edit_vendor/1",
                           data={"name": "Mathworks", "email": "mathworks_support@mathworks.com", "phone": "098768"},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b"Phone number must be 11 digits." in response.data
    with app.app_context():
        assert Vendor.query.count() == 1
        assert Vendor.query.first().email == "support@mathworks.com"  # The email should not have changed.
    assert response.request.path == "/edit_vendor/1"


def test_edit_owner(client, app):
    register(client)
    login(client)
    add_owner(client)
    response = client.post("/edit_owner/1",
                           data={"first_name": "John", "last_name": "Power", "email": "johnp@gmail.co.uk",
                                 "phone_extension": "5674"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Owner updated!" in response.data
    with app.app_context():
        assert Software_owner.query.count() == 1
        assert Software_owner.query.first().phone_extension == "5674"   # The phone extension should have changed.
    assert response.request.path == "/view_owner/1"


def test_edit_owner_invalid(client, app):
    register(client)
    login(client)
    add_owner(client)
    response = client.post("/edit_owner/1",
                           data={"first_name": "John", "last_name": "Power", "email": "johnp@gmail.co.uk",
                                 "phone_extension": "564a"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Phone extension must only contain numbers." in response.data
    with app.app_context():
        assert Software_owner.query.count() == 1
        assert Software_owner.query.first().phone_extension == "1234"  # The phone extension should not have changed.
    assert response.request.path == "/edit_owner/1"


def test_edit_software(client, app):
    register(client)
    login(client)
    add_vendor(client)
    add_owner(client)
    add_software(client)
    response = client.post("/edit_software/1",
                           data={"name": "MATLAB", "version": "R2023b", "expiry_date": "2024-12-31",
                                 "vendor": "1", "owner": "1"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Software updated!" in response.data
    with app.app_context():
        assert Software.query.count() == 1
        assert Software.query.first().version == "R2023b"   # The version should have changed.
    assert response.request.path == "/"


def test_edit_software_invalid(client, app):
    register(client)
    login(client)
    add_vendor(client)
    add_owner(client)
    add_software(client)
    response = client.post("/edit_software/1",
                           data={"name": "MATLAB", "version": "", "expiry_date": "2024-12-31",
                                 "vendor": "1", "owner": "1"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Entries must be greater than 1 character and less than 50." in response.data
    with app.app_context():
        assert Software.query.count() == 1
        assert Software.query.first().version == "R2020b"  # The version should not have changed.
    assert response.request.path == "/edit_software/1"


def test_create_admin_user(app):
    with app.app_context():
        admin = User(id="1", email="sandyt@gmail.com", password="Pandabear55", first_name="Sandy", last_name="Thomas",
                     admin=True)
        db.session.add(admin)
        db.session.commit()
        assert User.query.count() == 1
        assert User.query.first().admin == True


def create_admin_user(app):
    with app.app_context():
        pw = "Pandabear55"
        pw_hash = generate_password_hash(pw, method='sha256')
        admin = User(id="1", email="sandyt@gmail.com", password=pw_hash, first_name="Sandy", last_name="Thomas",
                     admin=True)
        db.session.add(admin)
        db.session.commit()


def test_admin_login(app, client):
    create_admin_user(app)
    respone = client.post("/login", data={"email": "sandyt@gmail.com", "password": "Pandabear55"},
                          follow_redirects=True)
    assert respone.status_code == 200
    assert b"Home" in respone.data
    assert respone.request.path == "/"  # should redirect to home page


def admin_login(client):
    return client.post("/login", data={"email": "sandyt@gmail.com", "password": "Pandabear55"}, follow_redirects=True)


def test_delete_vendor(client, app):
    create_admin_user(app)
    admin_login(client)
    add_vendor(client)
    response = client.post("/delete_vendor/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Vendor deleted!" in response.data
    with app.app_context():
        assert Vendor.query.count() == 0  # The vendor should have been deleted.
    assert response.request.path == "/all_vendors"


def test_unauthorised_delete_vendor(client, app):
    register(client)
    login(client)
    add_vendor(client)
    response = client.post("/delete_vendor/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"You do not have permission to delete vendors" in response.data
    with app.app_context():
        assert Vendor.query.count() == 1  # The vendor should not have been deleted.
    assert response.request.path == "/all_vendors"


def test_delete_owner(client, app):
    create_admin_user(app)
    admin_login(client)
    add_owner(client)
    response = client.post("/delete_owner/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Owner deleted!" in response.data
    with app.app_context():
        assert Software_owner.query.count() == 0  # The owner should have been deleted.
    assert response.request.path == "/all_owners"


def test_unauthorised_delete_owner(client, app):
    register(client)
    login(client)
    add_owner(client)
    response = client.post("/delete_owner/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"You do not have permission to delete owners" in response.data
    with app.app_context():
        assert Software_owner.query.count() == 1  # The owner should not have been deleted.
    assert response.request.path == "/all_owners"


def test_delete_software(client, app):
    create_admin_user(app)
    admin_login(client)
    add_vendor(client)
    add_owner(client)
    add_software(client)
    response = client.post("/delete_software/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Software deleted!" in response.data
    with app.app_context():
        assert Software.query.count() == 0  # The software should have been deleted.
    assert response.request.path == "/"


def test_unauthorised_delete_software(client, app):
    register(client)
    login(client)
    add_vendor(client)
    add_owner(client)
    add_software(client)
    response = client.post("/delete_software/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"You do not have permission to delete software" in response.data
    with app.app_context():
        assert Software.query.count() == 1  # The software should not have been deleted.
    assert response.request.path == "/"


def test_logout(client, app):
    register(client)
    login(client)
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
    assert response.request.path == "/login"    # should redirect to login page
