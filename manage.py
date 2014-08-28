from flask.ext.script import Manager, Command
from flask.ext.migrate import Migrate, MigrateCommand
from rvs.models import db
from rvs import app,models

class Init_App(Command):
    def run(self):
        db.create_all()
        u = models.User(username="admin",password="admin")
        db.session.add(u)
        u = models.User(username="test",password="test")
        db.session.add(u)
        db.session.commit()


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

manager.add_command('init', Init_App())

if __name__ == '__main__':
    manager.run()

