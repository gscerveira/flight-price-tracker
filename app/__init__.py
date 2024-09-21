from flask import Flask
from config import Config
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(Config)

CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


