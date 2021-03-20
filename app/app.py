from .models import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask import Flask


load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    db.init_app(app)
    migrate = Migrate(app, db)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app