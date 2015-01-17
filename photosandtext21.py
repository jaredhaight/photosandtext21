import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

pat2_env = os.environ.get('PAT2_ENV')
app = Flask(__name__)

if pat2_env == 'PROD':
    app.config.from_object('config.dev.Config')
else:
    app.config.from_object('config.dev.DevConfig')

db = SQLAlchemy(app)


