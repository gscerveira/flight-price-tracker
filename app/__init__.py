from flask import Flask
from config import Config
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from apscheduler.schedulers.background import BackgroundScheduler
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()
scheduler = BackgroundScheduler()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.tasks import init_scheduler, init_notification_service

    with app.app_context():
        init_scheduler(app)
        init_notification_service(app)

    from app import routes
    app.register_blueprint(routes.bp)
    
    swagger = Swagger(app, template_file='swagger.yaml', config={
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True, 
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "openapi": "3.0.2"
    })

    return app