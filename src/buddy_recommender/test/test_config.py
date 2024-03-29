import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app
from buddy_recommender.main.config import basedir, storedir


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('buddy_recommender.main.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] is 'buddy_secret_key')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' +
            os.path.join(basedir, storedir, 'buddy_recommender_main.db')
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('buddy_recommender.main.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] is 'buddy_secret_key')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' +
            os.path.join(basedir, storedir, 'buddy_recommender_test.db')
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('buddy_recommender.main.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
