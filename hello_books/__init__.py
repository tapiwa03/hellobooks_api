'''import dependancies'''
from flask_api import FlaskAPI
from cerberus import Validator
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand, Manager
import os
from flask import jsonify
from hello_books.config import app_config 
from flask_jwt_extended import JWTManager

db = SQLAlchemy()


def create_app(config_name):

    '''instantiate the app'''
    app = FlaskAPI(__name__)

    # set config
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])

    '''setup jwt for token encryption'''
    app.config['JWT_SECRET_KEY'] = 'Some-Key'
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
   
    '''JWT Manager'''
    jwt = JWTManager(app)
    blacklist = set()

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        '''check if token is blacklisted'''
        jti = decrypted_token['jti']
        return jti in blacklist


    # set up extensions
    db.init_app(app)

    '''import routes'''
    from hello_books.api.auth_views import auth
    from hello_books.api.book_views import books

    '''registering the routes to blueprints'''
    app.register_blueprint(auth)
    app.register_blueprint(books)

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})



    return app


