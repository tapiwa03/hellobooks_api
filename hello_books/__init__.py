#import flask
from flask import Flask

#import JWT web tokens
from flask_jwt_extended import (
  JWTManager
  )

#instantiate flask 
app = Flask(__name__)

#setup jwt for token encryption
app.config['JWT_SECRET_KEY'] = 'Some-Key'
jwt = JWTManager(app)

#import routes
from hello_books.api.auth_views import auth
from hello_books.api.book_views import books

#registering the routes to blueprints
app.register_blueprint(auth)
app.register_blueprint(books)
