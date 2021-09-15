import os

from flask import Flask
from core import db
from helpers import register_blueprints


def create_app(package_name, package_path, settings_override=None):
    """
    Returns a :class:`Flask` application instance for the Buddy recommender system
    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: configuration dict to be used when testing
    :return: configured :class:`Flask` application instance
    """
    app = Flask(package_name, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='mysecretdevkey',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if settings_override is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(settings_override)

    # ensure the instance folder and production config file exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    try:
        open(os.path.join(app.instance_path, 'config.py'), 'x').close()
    except OSError:
        pass

    db.init_app(app)
    register_blueprints(app, package_name, package_path)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
