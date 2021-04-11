from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SelectMultipleField, PasswordField, BooleanField, SubmitField, \
    IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class AuthorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Author')


class BookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    author = SelectField("Author", coerce=int, validate_choice=False)
    book_type = SelectField("Type", coerce=int, validate_choice=False)
    submit = SubmitField('Add Book')


class BookTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    rent_charge = FloatField('Rent Fee', validators=[DataRequired()])
    submit = SubmitField('Add Book Type')


class CustomerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Customer')


class RentBookForm(FlaskForm):
    customer = SelectField("customer", coerce=int, validate_choice=False)
    book = SelectMultipleField("Books", coerce=int, validate_choice=False)
    duration = IntegerField('No of Days', validators=[DataRequired()])
    submit = SubmitField('Rent Book')
