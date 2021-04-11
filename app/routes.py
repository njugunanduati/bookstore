from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_weasyprint import HTML, render_pdf
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.email import send_password_reset_email
from app.forms import LoginForm, BookForm, CustomerForm, AuthorForm, RegistrationForm, RentBookForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Book, Author, Customer, Rental


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/home')
@login_required
def index():
    rentals = Rental.query.all()
    return render_template('index.html', title='Home', rentals=rentals)


@app.route('/rent/book', methods=['GET', 'POST'])
@login_required
def rent_book():
    customers = [(i.id, f'{i.first_name} {i.last_name}') for i in Customer.query.all()]
    books = [(i.id, f'{i.title} @ ${i.rent_charge}') for i in Book.query.all()]
    form = RentBookForm()
    form.customer.choices = customers
    form.book.choices = books
    if form.validate_on_submit():
        for i in form.book.data:
            r = Rental(
                customer_id=form.customer.data,
                book_id=i,
                duration=form.duration.data
            )
            db.session.add(r)
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('rent_book.html', title='Rent A Book', form=form)


@app.route('/books')
@login_required
def get_books():
    books = Book.query.all()
    return render_template('books.html', title='Books', books=books)


@app.route('/add/book', methods=['GET', 'POST'])
@login_required
def add_book():
    authors = [(i.id, f'{i.first_name} {i.last_name}') for i in Author.query.all()]
    form = BookForm()
    form.author.choices = authors
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            rent_charge=form.rent_charge.data,
            author=form.author.data
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('get_books'))
    return render_template('add_book.html', title='Add Book', form=form)


@app.route('/authors')
@login_required
def get_authors():
    authors = Author.query.all()
    return render_template('authors.html', title='Authors', authors=authors)


@app.route('/add/author', methods=['GET', 'POST'])
@login_required
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('get_authors'))
    return render_template('add_author.html', title='Add Author', form=form)


@app.route('/customers')
@login_required
def get_customers():
    customers = Customer.query.all()
    return render_template('customers.html', title='Customers', customers=customers)


@app.route('/add/customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('get_customers'))
    return render_template('add_customer.html', title='Add Customer', form=form)


@app.route('/view/statement/<id>', methods=['GET'])
@login_required
def get_statement(id):
    rental = Rental.query.filter_by(id=id).first()
    return render_template('statement.html', title='Customer Receipt', rental=rental)


@app.route('/print/statement/<id>', methods=['GET'])
@login_required
def print_statement(id):
    rental = Rental.query.filter_by(id=id).first()
    html = render_template('statement.html', rental=rental)
    return render_pdf(HTML(string=html), download_filename=rental.get_customer())
