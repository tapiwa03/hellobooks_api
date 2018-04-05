'''import dependancies'''
from config import Config, app_config
from flask_api import FlaskAPI
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from cerberus import Validator

app = FlaskAPI(__name__)

'''Create DB'''
db = SQLAlchemy(app)
migrate = Migrate(app, db)
'''End of DB code'''


'''setup jwt for token encryption'''
app.config['JWT_SECRET_KEY'] = 'Some-Key'
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

'''import routes'''
from hello_books.api.auth_views import auth
from hello_books.api.book_views import books

'''registering the routes to blueprints'''
app.register_blueprint(auth)
app.register_blueprint(books)
