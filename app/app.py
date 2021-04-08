from app import app, db
from app.models import User, Book, Customer, Author


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Book': Book, 'Customer': Customer, 'Author': Author}
