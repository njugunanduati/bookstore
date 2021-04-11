import pytest
from app import app, db
from app.models import Author, Book, User, Customer, Rental, BookType


@pytest.fixture(scope='module')
def new_user():
    user = User('patkennedy79@gmail.com', 'FlaskIsAwesome')
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database tables
    db.create_all()

    # Insert user data
    u1 = User(username='patd', email='patd@gmail.com')
    u1.set_password('Toor')
    u2 = User(username='kennyg', email='kennyg@gmail.com')
    u2.set_password('PaSsWoRd')
    db.session.add([u1, u2])

    # Commit the changes for the users
    db.session.commit()

    # Insert author data
    a1 = Author(first_name='Pat', last_name='Dee', email='patd@gmail.com')
    a2 = Author(first_name='Kenny', last_name='Gee', email='kennyg@gmail.com')
    db.session.add([a1, a2])

    # Insert book type data
    bt1 = BookType(name='Regular', rent_charge='1.5')
    bt2 = BookType(name='Fiction', rent_charge='3.0')
    bt3 = BookType(name='Novel', rent_charge='1.5')
    db.session.add([bt1, bt2, bt3])

    # Insert book data
    b1 = Book(title='The River Between', book_type=bt1, author=a1)
    b2 = Book(title='The Man in the Mask', book_type=bt2, author=a2)
    db.session.add([b1, b2])

    # Insert customer data
    c1 = Customer(first_name='Jane', last_name='Doe', email='jane.doe@gmail.com')
    c2 = Customer(first_name='Jude', last_name='Law', email='jude.law@gmail.com')
    db.session.add([c1, c2])

    yield  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(username='patd', password='Toor'),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)
