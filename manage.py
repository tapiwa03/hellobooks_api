'''Script to run tests and create migrations'''
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api import create_app, db

app = create_app(config_name='development')

migrate = Migrate(app, db)
#create an instance of class to handle all commands
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def recreate_db():
    '''Destroy and Rebuild the Database currently in use'''
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
