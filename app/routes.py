from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    customer = {'first_name': 'James', 'last_name': 'Njuguna'}
    books = [
        {
            'author': {'first_name': 'John', 'last_name': 'Paul'},
            'title': 'Beautiful day in Portland',
            'rental_fee': 1,
            'duration': 4,
        },
        {
            'author': {'first_name': 'Chinua', 'last_name': 'Achebe'},
            'title': 'Things Fall Apart',
            'rental_fee': 1,
            'duration': 4,
        }
    ]
    return render_template('index.html', title='Home', customer=customer, books=books)
