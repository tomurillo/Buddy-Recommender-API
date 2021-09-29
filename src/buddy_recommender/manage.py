import os
import unittest

from flask_migrate import Migrate
from flask.cli import FlaskGroup

from .main import create_app, db

app = create_app(os.getenv('BOILERPLATE_ENV') or None)

app.app_context().push()

cli = FlaskGroup(create_app=create_app)

migrate = Migrate(app, db)


@cli.command()
def run():
    app.run()


@cli.command()
def test():
    """
    Runs all unit tests.
    """
    tests = unittest.TestLoader().discover('buddy_recommender/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()
