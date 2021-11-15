import unittest

from flask.cli import FlaskGroup

from buddy_recommender import blueprint
from buddy_recommender.main import create_app

app = create_app()
app.register_blueprint(blueprint)

cli = FlaskGroup(app)


@app.before_first_request
def populate_database():
    """
    Populate the database with initial data (i.e. admin account).
    This function runs only once, namely before the first request to this application instance
    :return:
    """
    import os
    from buddy_recommender.main import db
    from buddy_recommender.main.model.user import Account
    admin_email = os.getenv('ADMIN_EMAIL', 'test@example.com')
    admin_account = Account(
        email=admin_email,
        password=os.getenv('ADMIN_PWD', '123456'),
        admin=True
    )
    db.session.add(admin_account)
    db.session.commit()
    print(f'Admin account "{admin_email}" added to DB.')


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
