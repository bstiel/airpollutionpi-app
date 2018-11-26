import os
import sqlalchemy

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, scoped_session


# get settings from environment variables
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']


# configure Flask and extensions
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Flask error handlers
@app.errorhandler(IntegrityError)
def handle_error(e):
    return jsonify(error=str(e)), 400
