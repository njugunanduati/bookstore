from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class User(TimestampMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Customer(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return f'Customer {self.body} {self.last_name}'


class Author(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return f'Author {self.body} {self.last_name}'


class Book(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    rent_charge = db.Column(db.Numeric(5, 2))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __repr__(self):
        return f'Book {self.title}'

    def get_author(self):
        author = Author.query.filter_by(id=self.author).first()
        return f'{author.first_name} {author.last_name}'


class Rental(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    duration = db.Column(db.Integer)

    def __repr__(self):
        customer = Customer.query.filter_by(id=self.customer_id).first()
        book = Book.query.filter_by(id=self.book_id).first()
        return f'{book.title} has been rented by {customer.first_name} {customer.last_name}'

    def get_customer(self):
        customer = Customer.query.filter_by(id=self.customer_id).first()
        return f'{customer.first_name} {customer.last_name}'

    def get_title(self):
        book = Book.query.filter_by(id=self.book_id).first()
        return book.title

    def get_cost(self):
        book = Book.query.filter_by(id=self.book_id).first()
        return book.rent_charge * self.duration


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
