from flask import jsonify, Blueprint, request, abort, make_response, session
from flask_api import FlaskAPI
from flask.views import MethodView
from hello_books import app
from hello_books.api.models import HelloBooks

# instantiate blueprint and assign to var books
books = Blueprint('books', __name__)

hello_books = HelloBooks()


@app.route('/api/v1/books', methods=['POST'])
def add_book():
    sent_data = request.get_json(force=True)
    data = {
        'book_id': len(hello_books.books_list) + 1,
        'title': sent_data.get('title'),
        'author': sent_data.get('author'),
        'date_published': sent_data.get('date_published'),
        'genre': sent_data.get('genre'),
        'description': sent_data.get('description')
    }
    hello_books.add_book(data)

    response = jsonify({
        'book_id': data['book_id'],
        'title': data['title'],
        'author': data['author'],
        'date_published': data['date_published'],
        'genre': data['genre'],
        'description': data['description']
    })
    response.status_code = 201
    return response


@app.route('/api/v1/books/<int:id>', methods=['PUT'])
def edit_book():
    pass


@app.route('/api/v1/books/<int:id>', methods=['DELETE'])
def delete_book():
    pass


@app.route('/api/v1/books', methods=['GET'])
def get_all_books():
    return hello_books.view_books(), 200


@app.route('/api/v1/books/<int:id>', methods=['GET'])
def get_by_id(id):
    book = [book for book in hello_books.books_list if book['book_id'] == id]
    if len(book) == 0:
        return jsonify({'message': "Book Doesnt Exist"})
    return jsonify({'book': book[0]}), 200


# check if users is correct
@app.route('/api/v1/users/books', methods=['GET'])
def borrow_book():
    pass
