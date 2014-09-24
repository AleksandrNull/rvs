from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('rvs.config')
app.debug=True

from rvs import views, models
