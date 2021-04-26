from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from core import create_app

app = create_app(test_config=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

'''
"$ python testdb_migration.py db upgrade(downgrade)" - for upgrading(downgrading) test database
'''