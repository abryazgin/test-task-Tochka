from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')

# избавляемся от мусорных ворнингов
# https://github.com/mitsuhiko/flask-sqlalchemy/issues/365
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

import router
from database import models
