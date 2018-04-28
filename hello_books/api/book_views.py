'''import dependancies'''
import datetime
from flask import jsonify, Blueprint, request, make_response, session
from hello_books import app
from hello_books.models import HelloBooks, Books, Borrow
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, get_raw_jwt
)

blacklist = set()


jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    '''Check if token is blacklisted'''
    token_identifier = decrypted_token['jti']
    return token_identifier in blacklist


books = Blueprint('books', __name__)
hello_books = HelloBooks()



@app.route('/api/v1/books/<int:id>', methods=['PUT'])
@jwt_required
def edit_book(id):
    '''Function for editing book info'''
    if len(request.json) == 0:
        return jsonify({'message': "No data entered"})        
    if 'title' in request.json:
        title = request.json['title']
    else:
        title = None
    
    if 'author' in request.json:
        author = request.json['author']
    else:
        author = None
    
    if 'date_published' in request.json:
        date_published = request.json['date_published']
    else:
        date_published = None

    if 'genre' in request.json:
        genre = request.json['genre']
    else:
        genre = None
    
    if 'description' in request.json:
        description = request.json['description']
    else:
        description = None

    if 'isbn' in request.json:
        isbn = request.json['isbn']
    else:
        isbn = None

    if 'copies' in request.json:
        copies = request.json['copies']
    else:
        copies = None
    return Books().edit_book(
        title=title,
        author=author,
        date_published=date_published,
        genre=genre,
        description=description,
        isbn=isbn,
        copies=copies,
        book_id=id
    )
    
@app.route('/api/v1/books', methods=['POST'])
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
    if HelloBooks().add_book_validation(data) == True:
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



@app.route('/api/v1/users/books/<int:id>', methods=['POST', 'GET', 'PUT'])
@jwt_required
def borrow_book(id):
    '''function to retrieve current date'''
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


@app.route('/api/v1/books/<int:id>', methods=['DELETE'])
@jwt_required
def delete_book(id):
    '''function to delete book'''
    return Books().delete(id)


@app.route('/api/v1/books', methods=['GET'])
def get_all_books():
    '''function to get all books'''
    return Books().get_all()


@app.route('/api/v1/books/<int:id>', methods=['GET'])
def get_by_id(id):
    '''function to get a single book by its id'''
    if Books().get_by_id(id) == False:
        return jsonify({"message": "Book does not exist"}), 404
    else:
        return Books().get_by_id(id), 200
