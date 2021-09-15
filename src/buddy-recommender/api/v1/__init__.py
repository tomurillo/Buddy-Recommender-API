from functools import wraps

from flask import jsonify

from ... import app as shared_factory
from ...core import auth, BuddyError
from ...helpers import JSONEncoder


def create_app(settings_override=None):
    """
    Returns the Buddy-recommender API application instance
    """
    app = shared_factory.create_app(__name__, __path__, settings_override)

    app.json_encoder = JSONEncoder

    app.errorhandler(BuddyError)(on_api_error)
    app.errorhandler(404)(on_404)

    return app


def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @auth.login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]
            return jsonify(dict(data=rv)), sc
        return f

    return decorator


@auth.verify_password
def verify_password(username, password):
    if username == 'testusername' and password == 'testpasword':
        return True
    return False


def on_api_error(e):
    """
    Custom API error handler that returns the error as JSON
    """
    return jsonify(dict(error=e.msg)), 400


def on_404(e):
    """
    Custom API 404 error handler that the returns the error as JSON
    """
    return jsonify(dict(error='Not found')), 404
