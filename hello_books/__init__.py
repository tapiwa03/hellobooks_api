#import flask
from flask import Flask

#instantiate flask 
app = Flask(__name__)

#import routes
from hello_books.api.auth_views import auth
#from hello_books.api.book_views import *

#registering the routes to blueprints
app.register_blueprint(auth)
