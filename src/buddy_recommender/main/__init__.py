import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
migrate = Migrate()


def create_app(script_info=None):
    new_app = Flask(__name__)
    config_type = os.getenv('FLASK_ENV') or 'development'
    config_obj = config_by_name[config_type]
    new_app.config.from_object(config_obj)
    db.init_app(new_app)
    flask_bcrypt.init_app(new_app)
    migrate.init_app(new_app, db)

    @new_app.shell_context_processor
    def shell_context():
        return {'app': new_app, 'db': db}

    return new_app
