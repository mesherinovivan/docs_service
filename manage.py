from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import app, db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='localhost', port=5000,use_debugger=True))

if __name__ == '__main__':
    manager.run()