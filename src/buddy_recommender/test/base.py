from flask_testing import TestCase

from buddy_recommender.main import db
from manage import app

API_VERSIONS = ['v1']


class BaseTestCase(TestCase):
    """
    Base Test Case with scaffolding utils
    """

    def create_app(self):
        app.config.from_object('buddy_recommender.main.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
