from app.models import User, Author, Book, Customer


def test_new_user():
    """
    test new user
    """
    user = User(username='patkennedy79', email='patkennedy79@gmail.com')
    user.set_password('FlaskIsAwesome')
    assert user.username == 'patkennedy79'
    assert user.email == 'patkennedy79@gmail.com'
    assert user.password_hash != 'FlaskIsAwesome'


def test_new_author():
    """
    test new book
    """
    author = Author(first_name='Pat', last_name='Dee', email='patd@gmail.com')
    assert author.first_name == 'Pat'
    assert author.last_name == 'Dee'
    assert author.email == 'patd@gmail.com'


def test_new_book():
    """
    test new book
    """
    author = Author(first_name='Pat', last_name='Dee', email='patd@gmail.com')
    book = Book(title='The River Between', rent_charge=1, author=author.id)
    assert book.title == 'The River Between'
    assert book.author == author.id


def test_new_customer():
    """
    test new customer
    """
    customer = Customer(first_name='Jane', last_name='Doe', email='jane.doe@gmail.com')
    assert customer.first_name == 'Jane'
    assert customer.last_name == 'Doe'
    assert customer.email == 'jane.doe@gmail.com'
