'''import dependancies for script migrations'''
from flask_migrate import Manager
from flask_script import Migrate, MigrateCommand
from hello_books import db, app

app = app(app_config="development")
migrate = Migrate(app, db)
manager = Manager(app)


manager.add_command('db', MigrateCommand)


if __name__ == '__main___':
    manager.run()
    