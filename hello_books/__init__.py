#import flask
from flask_api import FlaskAPI
#import JWT web tokens
from flask_jwt_extended import (
  JWTManager
  )
from cerberus import Validator
#instantiate flask 
app = FlaskAPI(__name__)

#setup jwt for token encryption
app.config['JWT_SECRET_KEY'] = 'Some-Key'
app.config["PROPAGATE_EXCEPTIONS"]= True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

#import routes
from hello_books.api.auth_views import auth
from hello_books.api.book_views import books

#registering the routes to blueprints
app.register_blueprint(auth)
app.register_blueprint(books)
