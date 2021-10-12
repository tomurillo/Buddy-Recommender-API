import unittest

from buddy_recommender.main import db
from buddy_recommender.main.model.user import Account
from buddy_recommender.test.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = Account(
            email='test@example.com',
            password='*123*SuperSecurePassword$321$',
        )
        db.session.add(user)
        db.session.commit()
        auth_token = Account.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))

    def test_decode_auth_token(self):
        user = Account(
            email='test@example.com',
            password='*123*SuperSecurePassword$321$',
        )
        db.session.add(user)
        db.session.commit()
        auth_token = Account.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))
        self.assertTrue(Account.decode_auth_token(auth_token) == 1)


if __name__ == '__main__':
    unittest.main()
