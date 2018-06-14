from flask.cli import FlaskGroup
import unittest
from hello_books import create_app, db
from hello_books.models.validate_model import HelloBooks
from hello_books.models.book_model import Books
from hello_books.models.user_model import User
from hello_books.models.borrow_model import Borrow
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = create_app(config_name='development')

migrate = Migrate(app, db)
#create an instance of class to handle all commands
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()



@manager.command
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('hello_books/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
