'''import dependancies'''
from flask_api import FlaskAPI
from cerberus import Validator
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand, Manager
from flask import jsonify, Flask, make_response
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from api.config import app_config
from flask_cors import CORS

db = SQLAlchemy()
flask_mail = Mail()

def create_app(config_name):

    '''instantiate the app'''
    app = FlaskAPI(__name__)
    CORS(app)
    # set config
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    flask_mail.init_app(app)
    #setup jwt for token encryption'''
    app.config['JWT_SECRET_KEY'] = 'Some-Key'
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    #JWT Manager'''
    jwt = JWTManager(app)
    blacklist = set()
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(self):
        '''check if token is blacklisted'''
        pass
    #import routes
    from api.views.auth import auth
    from api.views.book import books
    #registering the routes to blueprints
    app.register_blueprint(auth)
    app.register_blueprint(books)
    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})
    return app
