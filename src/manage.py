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
    from dotenv import load_dotenv
    from flask import abort
    from buddy_recommender.main.service.util import save_changes
    from buddy_recommender.main.service.account_service import get_account
    from buddy_recommender.main.model.user import Account
    import sqlite3
    load_dotenv()
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_pwd = os.getenv('ADMIN_PWD')
    if admin_email and admin_pwd:
        if not get_account(admin_email):
            admin_account = Account(
                email=admin_email,
                password=admin_pwd,
                admin=True
            )
            try:
                save_changes(admin_account)
                app.logger.info('Admin account "%s" added to DB.', admin_email)
            except sqlite3.OperationalError as e:
                app.logger.error('Database error: %s.', str(e))
                abort(500)
    else:
        app.logger.error('Missing environment variables ADMIN_EMAIL and/or ADMIN_PWD')
        abort(500)


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
