'''import dependancies'''
import datetime
from flask import jsonify, Blueprint, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
    get_raw_jwt
)
from api.models.validate import HelloBooks
from api.models.book import Books
from api.models.borrow import Borrow
from api.models.blacklist import Blacklist
from api.views.auth import default_parameters

books = Blueprint('books', __name__)

@books.route('/api/v1/books/<int:id>', methods=['PUT'])
@jwt_required
def edit_book(id):
    '''Function for editing book info'''
    if len(request.json) is 0:
        return jsonify({'message': "No data entered"}), 400
    fields = {
        'title': None,
        'author': None,
        'date_published': None,
        'genre': None,
        'description': None,
        'isbn': None,
        'copies': None}
    for key in fields:
        if '%s' % key in request.json:
            fields[key] = request.json['%s' % key]
        else:
            key = None
    return Books().edit_book(
        title=fields['title'],
        author=fields['author'],
        date_published=fields['date_published'],
        genre=fields['genre'],
        description=fields['description'],
        isbn=fields['isbn'],
        copies=fields['copies'],
        book_id=id
    )

@books.route('/api/v1/books', methods=['POST'])
@jwt_required
def add_book():
    '''Function to add a book'''
    sent_data = request.get_json(force=True)
    raw_data = {
        'title': sent_data.get('title'),
        'author': sent_data.get('author'),
        'date_published': sent_data.get('date_published'),
        'genre': sent_data.get('genre'),
        'description': sent_data.get('description'),
        'isbn': sent_data.get('isbn'),
        'copies': sent_data.get('copies')
    }
    data = {k : v.strip() for k, v in raw_data.items()}
    if HelloBooks().add_book_validation(data) is True:
        return Books().add_book(
            title=data['title'],
            author=data['author'],
            date_published=data['date_published'],
            genre=data['genre'],
            description=data['description'],
            isbn=data['isbn'],
            copies=data['copies'],
            date_created=datetime.datetime.now()
        )
    else:
        return jsonify({"message": "Please enter correct book details"})

@books.route('/api/v1/books/<int:id>', methods=['DELETE'])
@jwt_required
def delete_book(id):
    '''function to delete book'''
    return Books().delete(id)

@books.route('/api/v1/books', methods=['GET'])
@jwt_required
def get_all_books():
    '''function to get all books'''
    parameters = default_parameters()
    return Books().get_all(page=parameters[0], per_page=parameters[1])

@books.route('/api/v1/books/<int:id>', methods=['GET'])
@jwt_required
def get_by_book_id(id):
    '''function to get a single book by its id'''
    Books().check_if_book_exists(id)
    return Books().get_by_id(id)

@books.route('/api/v1/users/books/<int:id>', methods=['POST'])
@jwt_required
def borrow_book(id):
    '''function to borrow a book'''
    email = get_jwt_identity()
    now = datetime.datetime.now()
    sent_data = request.get_json(force=True)
    return Borrow().borrow_book(
        book_id=id,
        user_email=email,
        borrow_date=now.strftime("%d/%m/%Y"),
        due_date=sent_data.get('due_date'),
        return_date=None
    )

@books.route('/api/v1/users/books/<int:id>', methods=['PUT'])
@jwt_required
def return_book(id):
    '''function to return a book'''
    email = get_jwt_identity()
    time = datetime.datetime.today().strftime('%d/%m/%Y')
    return Borrow().return_book(
        borrow_id=id,
        user_email=email,
        return_date=time
    )

@books.route('/api/v1/users/books', methods=['GET'])
@jwt_required
def get_borrowing_history():
    '''function to get a users full borrowing history'''
    email = get_jwt_identity()
    #endpoint for retrieving books not returned "/api/v1/users/books?returned=false"
    if 'returned' in request.args:
        if request.args['returned'] == 'false':
            return Borrow().books_not_returned(user_email=email)
    parameters = default_parameters()
    return Borrow().borrowing_history(
        user_email=email,
        page=parameters[0],
        per_page=parameters[1])

@books.route('/api/v1/users/books/all', methods=['GET'])
@jwt_required
def books_currently_out():
    '''function to get a users full borrowing history'''
    #entry format /api/v1/users/books/all?page=1&results=2
    parameters = default_parameters()
    return Borrow().books_currently_out(page=parameters[0], per_page=parameters[1])
