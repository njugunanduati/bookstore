from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_weasyprint import HTML, render_pdf
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.email import send_password_reset_email
from app.forms import LoginForm, BookForm, CustomerForm, AuthorForm, RegistrationForm, RentBookForm, \
    ResetPasswordRequestForm, ResetPasswordForm, BookTypeForm, CustomPricingForm, ConditionPricingForm
from app.models import User, Book, BookType, Author, Customer, Rental, CustomPricing, ConditionPricing


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
    books = [(i.id, f'{i.title} @ ${i.get_rent_charge()}') for i in Book.query.all()]
    book_type = BookType.query.all
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


@app.route('/book/types')
@login_required
def get_book_types():
    book_types = BookType.query.all()
    return render_template('book_types.html', title='BookTypes', book_types=book_types)


@app.route('/add/book/type', methods=['GET', 'POST'])
@login_required
def add_book_type():
    form = BookTypeForm()
    if form.validate_on_submit():
        book_type = BookType(
            name=form.name.data,
            rent_charge=form.rent_charge.data,
        )
        db.session.add(book_type)
        db.session.commit()
        return redirect(url_for('get_book_types'))
    return render_template('add_book_type.html', title='Add Book', form=form)


@app.route('/edit/book/type/<id>', methods=['GET', 'POST'])
@login_required
def edit_book_type(id):
    book_type = BookType.query.filter_by(id=id).first()
    form = BookTypeForm()
    if form.validate_on_submit():
        book_type.name = form.name.data,
        book_type.rent_charge = form.rent_charge.data,
        book_type.custom_pricing = form.custom_pricing.data
        db.session.commit()
        flash('Book Type has been updated.')
        return redirect(url_for('get_book_types'))
    book_type = BookType.query.filter_by(id=id).first()
    form.name.data = book_type.name
    form.rent_charge.data = book_type.rent_charge
    form.custom_pricing.data = book_type.custom_pricing
    return render_template('edit_book_type.html', title='Save Book Type', form=form)


@app.route('/books')
@login_required
def get_books():
    books = Book.query.all()
    return render_template('books.html', title='Books', books=books)


@app.route('/add/book', methods=['GET', 'POST'])
@login_required
def add_book():
    authors = [(i.id, f'{i.first_name} {i.last_name}') for i in Author.query.all()]
    book_types = [(i.id, f'{i.name} {i.rent_charge}') for i in BookType.query.all()]
    form = BookForm()
    form.author.choices = authors
    form.book_type.choices = book_types
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            book_type=form.book_type.data,
            author=form.author.data
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('get_books'))
    return render_template('add_book.html', title='Add Book', form=form)


@app.route('/edit/book/<id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    book = Book.query.filter_by(id=id).first()
    authors = [(i.id, f'{i.first_name} {i.last_name}') for i in Author.query.all()]
    book_types = [(i.id, f'{i.name} {i.rent_charge}') for i in BookType.query.all()]
    form = BookForm()
    form.author.choices = authors
    form.book_type.choices = book_types
    if form.validate_on_submit():
        book.title = form.title.data,
        book.book_type = form.book_type.data,
        book.author = form.author.data
        db.session.commit()
        flash('Book has been updated.')
        return redirect(url_for('get_books'))
    book = Book.query.filter_by(id=id).first()
    form.title.data = book.title
    form.author.data = book.author
    return render_template('edit_book.html', title='Save Book', form=form)


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


@app.route('/custom/pricing')
@login_required
def get_custom_pricing():
    custom_prices = CustomPricing.query.all()
    return render_template('custom_pricing.html', title='CustomPricing', custom_prices=custom_prices)


@app.route('/add/custom/pricing/<book_type_id>', methods=['GET', 'POST'])
@login_required
def add_custom_pricing(book_type_id):
    book_type = BookType.query.filter_by(id=book_type_id).first()
    form = CustomPricingForm()
    if form.validate_on_submit():
        custom_price = CustomPricing(
            book_type=book_type.id,
            minimum_charge=form.minimum_charge.data,
            no_of_days=form.no_of_days.data,
        )
        db.session.add(custom_price)
        db.session.commit()
        return redirect(url_for('get_custom_pricing'))
    return render_template('add_custom_pricing.html', title='Add Custom Pricing', form=form)


@app.route('/edit/custom/pricing/<id>', methods=['GET', 'POST'])
@login_required
def edit_custom_pricing(id):
    custom_pricing = CustomPricing.query.filter_by(id=id).first()
    form = CustomPricingForm()
    if form.validate_on_submit():
        custom_pricing.book_type = form.book_type.data,
        custom_pricing.minimum_charge = form.minimum_charge.data,
        custom_pricing.no_of_days = form.no_of_days.data
        db.session.commit()
        flash('Custom Pricing has been updated.')
        return redirect(url_for('get_book_types'))
    custom_pricing = CustomPricing.query.filter_by(id=id).first()
    form.name.data = custom_pricing.book_type
    form.minimum_charge.data = custom_pricing.minimum_charge
    form.no_of_days.data = custom_pricing.no_of_days
    return render_template('edit_custom_pricing.html', title='Save Custom Pricing', form=form)


@app.route('/condition/pricing')
@login_required
def get_condition_pricing():
    condition_prices = ConditionPricing.query.all()
    return render_template('conditions.html', title='CustomPricing', condition_prices=condition_prices)


@app.route('/add/condition/pricing', methods=['GET', 'POST'])
@login_required
def add_condition_pricing():
    form = ConditionPricingForm()
    if form.validate_on_submit():
        cp = ConditionPricing(
            condition=form.condition.data,
        )
        db.session.add(cp)
        db.session.commit()
        return redirect(url_for('get_custom_pricing'))
    return render_template('add_condition.html', title='Add Condition Pricing', form=form)