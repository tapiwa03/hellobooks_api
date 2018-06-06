from flask_testing import TestCase
from hello_books import create_app, db
from hello_books.config import app_config

app = create_app('testing')

class BaseTestCase(TestCase):


    def create_app(self):
        app.config.from_object(app_config['testing'])
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
