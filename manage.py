from rvs import app,db,models 
from flask.ext.script import Manager, Command
from flask.ext.migrate import Migrate, MigrateCommand


class Init_App(Command):
    def run(self):
        db.create_all()
        u = models.User(name="admin",passwd="admin")
        db.session.add(u)
        db.session.commit()

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

manager.add_command('init', Init_App())

if __name__ == '__main__':
    manager.run()

