import unittest
import json

from buddy_recommender.main import db
from buddy_recommender.main.model.blacklisttoken import BlacklistToken
from buddy_recommender.test.base import BaseTestCase

ACCOUNT_EMAIL = 'test@example.com'
ACCOUNT_PWD = 'myPassword%*123'


def create_account(self):
    return self.client.post(
        '/account/',
        data=json.dumps({
            'email': ACCOUNT_EMAIL,
            'password': ACCOUNT_PWD,
        }),
        content_type='application/json'
    )


def login(self, email=ACCOUNT_EMAIL, pwd=ACCOUNT_PWD):
    return self.client.post(
        '/auth/login',
        data=json.dumps({
            'email': email,
            'password': pwd,
        }),
        content_type='application/json'
    )


def logout(self, auth_token):
    return self.client.post('/auth/logout', headers=dict(Authorization=f'Bearer {auth_token}'))


def create_account_and_validate(self):
    """
    Create a new account for testing protected endpoints
    :param self: TestCase instance
    :return: Login response dictionary
    """
    create_account(self)
    response = login(self)
    self.assertEqual(response.status_code, 200)
    login_data = json.loads(response.data.decode())
    auth_token = login_data['Authorization']
    self.assertTrue(auth_token)
    return login_data


class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        """
        Test for new account registration
        """
        with self.client:  # Keep request context for the whole test
            response = create_account(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_register_existing(self):
        """
        Test for trying to register with an already existing account
        """
        create_account(self)
        with self.client:
            response = create_account(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Account already exists. Log in or use a different email address.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)

    def test_login(self):
        """
        Test for login with an existing account
        """
        with self.client:
            # Register new account
            create_account(self)
            # Log in with created account
            response = login(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_login_no_account(self):
        """
        Test for login attempt for a non-existing account
        """
        with self.client:
            response = login(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'email does not exist')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_login_wrong_password(self):
        """
        Test for login attempt for an existing account with the wrong password
        """
        with self.client:
            create_account(self)
            response = login(self, pwd='aDifferentPassword')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'wrong password')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_login_wrong_email(self):
        """
        Test for login attempt with the wrong email
        """
        with self.client:
            create_account(self)
            response = login(self, email='some_mail@example.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'email does not exist')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_logout(self):
        """
        Test for a correct user logout
        """
        with self.client:
            login_data = create_account_and_validate(self)
            response = logout(self, login_data['Authorization'])
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_blacklisted_logout(self):
        """
        Test for account logout after being blacklisted
        """
        with self.client:
            login_data = create_account_and_validate(self)
            auth_token = login_data['Authorization']
            blacklist_token = BlacklistToken(token=auth_token)
            db.session.add(blacklist_token)
            db.session.commit()
            response = logout(self, auth_token)
            logout_data = json.loads(response.data.decode())
            self.assertTrue(logout_data['status'] == 'fail')
            self.assertTrue(logout_data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
