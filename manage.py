from flask_script import Manager, Shell
from app import create_app, db
from app.models import User,LoginLog
from flask_migrate import Migrate, MigrateCommand, upgrade
#from flask.ext.sqlalchemy import SQLAlchemy

app = create_app('default')

#db = SQLAlchemy(app)

manager = Manager(app,db)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app, db=db, User=User,LoginLog=LoginLog)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
