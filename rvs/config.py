import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'reservation.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SECRET_KEY = 'E\x80y\xfc\xc3\x08\x8b\xe1\x00\x1f_\x89\xd14\xec\xe8T\x89:"e\xbc\xecq'
