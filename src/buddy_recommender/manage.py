import unittest

from flask.cli import FlaskGroup

from main import app

cli = FlaskGroup(app)


@cli.command('test')
def test():
    """
    Runs all unit tests.
    """
    tests = unittest.TestLoader().discover('buddy_recommender/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    cli()
