from dotenv import load_dotenv
import os
from flask import Flask
from .routes import user
feat/post-use-cases


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DSN=os.getenv('DSN'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(user.user_blueprint)
    return app
