import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from xkcd import app
from xkcd.app import create_app
from xkcd.database import db

MIGRATION_DIR = os.path.join('app', 'migrations')

migrate = Migrate(app, db)
#manager = Manager(app)
manager = Manager(create_app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()