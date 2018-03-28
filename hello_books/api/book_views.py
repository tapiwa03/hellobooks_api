
from flask import jsonify, Blueprint, request, Flask
from flask.views import MethodView
from hello_books import app
from hello_books.api.models import HelloBooks

#instantiate blueprint and assign to var books 
books = Blueprint('books', __name__)

initHelloBooks = HelloBooks()
 
@app.route('/api/v1/books', methods=['POST'])
def add_book():
    sent_data = request.get_json(force = True)
    data = {
      'book_id' : len(initHelloBooks.books_list) + 1,
      'title':'War and Peace',
      'author': 'Leo Tolstoy',
      'date_published': '02/12/2008',
      'genre':'fiction',
      'description':'This is a description about the book war and peace by leo tolstoy'
    }
    return initHelloBooks.add_book(data), 201


@app.route('/api/v1/books/<int:id>', methods=['PUT'])
def edit_book():
    pass

@app.route('/api/v1/books/<int:id>', methods=['DELETE'])
def delete_book():
    pass

@app.route('/api/v1/books/', methods=['GET'])
def get_all_books():
    pass

@app.route('/api/v1/books/<int:id>', methods=['GET'])
def get_book_by_id():
    pass

#check if users is correct
@app.route('/api/v1/users/books/', methods=['GET'])
def borrow_book():
    pass