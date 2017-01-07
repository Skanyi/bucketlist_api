import os
from flask_script import Manager
from config.config import Config
from flask_migrate import Migrate, MigrateCommand
from app import app, db


app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
