import unittest

from flask.cli import FlaskGroup

from buddy_recommender.main import create_app

app = create_app()
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
