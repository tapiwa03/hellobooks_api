'''import dependancies'''
import datetime
from flask import jsonify, Blueprint, request, make_response, session
from hello_books import app
from hello_books.api.models import HelloBooks
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
    book = [book for book in hello_books.books_list if book['book_id'] == id]
    if len(book) == 0:
        return jsonify({'message': "Book Doesn't Exist"})
    if not request.json:
        return jsonify({'message': "No data entered"}), 204
    '''Check if title is entered and if it is correct'''
    if 'title' in request.json:
        title = request.json['title'].strip()
        if hello_books.edit_book_validation({'title': title}) == True:
            book[0]['title'] = title
        else:
            return jsonify(
                {'message': 'Please enter a correct title above 4 characters'})
    '''check if author is entered and if it is correct'''
    if 'author' in request.json:
        author = request.json['author'].strip()
        if hello_books.edit_book_validation({'author': author}) == True:
            book[0]['author'] = author
        else:
            return jsonify(
                {'message': 'Please enter a correct author above 4 characters'})
    '''check if date is correctly entered'''
    if 'date_published' in request.json:
        date = request.json['date_published'].strip()
        if hello_books.date_validate(date) == True:
            book[0]['date_published'] = date
        else:
            return jsonify(
                {'message': 'Please enter a correct date format DD-MM-YYYY'})
    '''check if genre is entered correctly'''
    if 'genre' in request.json:
        genre = request.json['genre'].strip()
        if hello_books.edit_book_validation({'genre': genre}) == True:
            book[0]['genre'] = genre
        else:
            return jsonify(
                {"message": "Please enter a genre between 4-10 characters"})
    '''check if description entered correctly'''
    if 'description' in request.json:
        description = request.json['description'].strip()
        if hello_books.edit_book_validation(
                {'description': description}) == True:
            book[0]['description'] = description
        else:
            return jsonify(
                {'message': "Description should be between 4-200 characters"})
    if hello_books.edit_book_validation(book[0]) == True:
        return jsonify({'book': book[0]})
    else:
        return jsonify({"message": "Please enter book data correctly"})


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
        'description': sent_data.get('description')
    }
    data = {k.strip() : v.strip() for k, v in raw_data.items()}
    if HelloBooks().add_book_validation(data) == True:
        hello_books.add_book(data)
        response = jsonify({
            'book_id': data['book_id'],
            'title': data['title'],
            'author': data['author'],
            'date_published': data['date_published'],
            'genre': data['genre'],
            'description': data['description'],
            'available': True
        })
        response.status_code = 201
        return response
    else:
        return jsonify({"message": "Please enter correct book details"})


# check if users is correct
@app.route('/api/v1/users/books/<int:id>', methods=['POST', 'GET', 'PUT'])
@jwt_required
def borrow_book(id):
    '''function to retrieve current date'''
    now = datetime.datetime.now()
    email = get_jwt_identity()
    book = [book for book in hello_books.books_list if book['book_id'] == id]
    # add data to dictionary
    sent_data = request.get_json(force=True)
    data = {
        'book_id': id,
        'user_email': email,
        'borrow_date': now.strftime("%d/%m/%Y"),
        'due_date': sent_data.get('due_date'),
        'return_date': ""
    }

    if len(book) == 0:
        return jsonify({'message': "Book Doesnt Exist"}), 404
    elif book[0]['available'] == False:
        return jsonify({'message': "The book has already been borrowed"}), 409
    else:
        book[0]['available'] = False
        HelloBooks().borrow_book(data)
        response = jsonify({
            'book_id': data['book_id'],
            'user': data['user_email'],
            'borrow_date': data['borrow_date'],
            'due_date': data['due_date'],
            'return_date': data['return_date']
        })
        response.status_code = 201
        return response


@app.route('/api/v1/books/<int:id>', methods=['DELETE'])
@jwt_required
def delete_book(id):
    '''function to delete book'''
    book = [book for book in hello_books.books_list if book['book_id'] == id]
    if len(book) == 0:
        return jsonify({'message': "Book Doesnt Exist"})
    hello_books.books_list.remove(book[0])
    return jsonify({'message': "Book Was Deleted"})


@app.route('/api/v1/books', methods=['GET'])
def get_all_books():
    '''function to get all books'''
    return hello_books.view_books(), 200


@app.route('/api/v1/books/<int:id>', methods=['GET'])
def get_by_id(id):
    '''function to get a single book by its id'''
    book = [book for book in hello_books.books_list if book['book_id'] == id]
    if len(book) == 0:
        return jsonify({'message': "Book Doesnt Exist"}), 404
    return jsonify({'book': book[0]}), 200
