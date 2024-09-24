from flask import Flask
from config import Config
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)

app.config.from_object(Config)

CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create the database if it doesn't exist
with app.app_context():
    if not database_exists(db.engine.url):
        create_database(db.engine.url)
        print("Database created.")
    else:
        print("Database already exists.")

from app import models, routes