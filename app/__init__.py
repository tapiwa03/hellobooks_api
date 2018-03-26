# import flask api
from flask_api import FlaskAPI

from flask import Flask, jsonify, abort, make_response, request, json

# local import
from instance.config import app_config

#list of books to be used
books_list= [
    {
        'book_id':'1',
        'title':'War and Peace',
        'author': 'Leo Tolstoy',
        'date_published': '02/12/2008',
        'genre':'fiction',
        'description':'This is a description about the book war and peace by leo tolstoy'
    },
]

users_list = [{
  'email': 'test@mail.com',
  'password' : 'test123'
  },
  {
  'email': 'user@mail.com',
  'password' : 'user123'
  }
]

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')


    #show all books
    @app.route('/api/books', methods=[ 'GET'])
    def books_get():
      return jsonify({'book': books_list})


    @app.route('/api/books', methods=['POST'])
    # creates a new book, from the data that is provided with the request
    def create_book():
      # request.json, request the JSON marked data and nothing else
      data = request.get_json(force=True)
      new_book = {
        'book_id': len(books_list) + 1,
        'title': data.get('title'),
        'author': data.get('author'),
        'date_published': data.get('date_published'),
        'genre': data.get('genre'),
        'description': data.get('description'),
        }
      # append new books to the books array
      books_list.append(new_book)
      # send back a 201 code which is defined as Created
      return make_response(jsonify({'book': book}), 201)


   









    return app


