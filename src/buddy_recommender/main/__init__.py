from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
migrate = Migrate()


def create_app(script_info=None):
    app = Flask(__name__)
    if script_info is None:
        script_info = config_by_name['dev']
    app.config.from_object(script_info)
    db.init_app(app)
    flask_bcrypt.init_app(app)
    migrate.init_app(app, db)

    @app.shell_context_processor
    def shell_context():
        return {'app': app, 'db': db}

    return app