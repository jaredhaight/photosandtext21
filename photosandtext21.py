import os
from flask import Flask
from flask.ext.mongoengine import MongoEngine

pat2_env = os.environ.get('PAT2_ENV')
app = Flask(__name__)

if pat2_env == 'PROD':
    app.config.from_object('config.prod.ProdConfig')
else:
    app.config.from_object('config.dev.DevConfig')

db = MongoEngine(app)


