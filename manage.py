from app import app, db
from flask_migrate import Migrate, MigrateCommand
#flask_script
from flask_script import Manager

#flask_script manager
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
