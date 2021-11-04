import json

from buddy_recommender.test.base import BaseTestCase, API_VERSIONS
from buddy_recommender.test.test_auth import register_and_login, admin_register_and_login


def add_rating(self, user_id, item_id, rating, auth_token, api_version):
    headers = dict(Authorization=f'Bearer {auth_token}') if auth_token else None
    payload = {'user_id': user_id,
               'item_id': item_id}
    if rating is not None:
        payload['rating'] = rating
    return self.client.post(
        f'/api/{api_version}/rating/',
        data=json.dumps(payload),
        headers=headers,
        content_type='application/json'
    )


class TestRatingBlueprint(BaseTestCase):
    def test_add_rating(self):
        """
        Test for adding a new rating
        """
        with self.client:
            login_data = register_and_login(self)
            auth_token = login_data['Authorization']
            # Add new rating
            response = add_rating(self, 1, 2, 5, auth_token, API_VERSIONS[0])
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'New rating added.')
            # Retrieve added rating
            response = self.client.get(f'/api/{API_VERSIONS[0]}/rating/user/1/item/2',
                                       headers=dict(Authorization=f'Bearer {auth_token}'))
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_data['data']['user_id'], 1)
            self.assertEqual(response_data['data']['item_id'], 2)
            self.assertEqual(response_data['data']['rating'], 5)
            self.assertTrue(response_data['data']['created'])
            self.assertTrue(response_data['data']['updated'])
            # Same request, change parameter order
            response = self.client.get(f'/api/{API_VERSIONS[0]}/rating/item/2/user/1',
                                       headers=dict(Authorization=f'Bearer {auth_token}'))
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_data['data']['item_id'], 2)
            self.assertEqual(response_data['data']['user_id'], 1)
            self.assertEqual(response_data['data']['rating'], 5)
            self.assertTrue(response_data['data']['created'])
            self.assertTrue(response_data['data']['updated'])

    def test_missing_rating(self):
        """
        Test for requesting a non-existing rating
        """
        with self.client:
            login_data = register_and_login(self)
            auth_token = login_data['Authorization']
            # Add new rating
            response = add_rating(self, 1, 2, 5, auth_token, API_VERSIONS[0])
            self.assertEqual(response.status_code, 201)
            # Request rating not in database
            response = self.client.get(f'/api/{API_VERSIONS[0]}/rating/user/1/item/3',
                                       headers=dict(Authorization=f'Bearer {auth_token}'))
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'][:32] == 'No rating for user 1 and item 3.')

    def test_rating_no_auth(self):
        """
        Test for unauthorized requests
        """
        fake_auth_token = 'asdf123'
        with self.client:
            register_and_login(self)
            # No token
            response = add_rating(self, 1, 2, 5, None, API_VERSIONS[0])
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'Provide a valid auth token.')
            # Invalid token
            response = add_rating(self, 1, 2, 5, fake_auth_token, API_VERSIONS[0])
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'Invalid token. Please log in again.')

    def test_get_full_matrix(self):
        """
        Test for fetching the whole user-item rating matrix (admins only)
        """
        with self.client:
            # Create admin account and login
            login_data = admin_register_and_login(self)
            auth_token = login_data['Authorization']
            # Return all (zero) ratings
            response = self.client.get(f'/api/{API_VERSIONS[0]}/rating/',
                                       headers=dict(Authorization=f'Bearer {auth_token}'))
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data.decode())
            self.assertEqual(len(response_data['data']), 0)
            # Add a few ratings
            add_rating(self, 1, 2, 5, auth_token, API_VERSIONS[0])
            add_rating(self, 1, 3, 1, auth_token, API_VERSIONS[0])
            add_rating(self, 2, 8, 3, auth_token, API_VERSIONS[0])
            # Return all ratings
            response = self.client.get(f'/api/{API_VERSIONS[0]}/rating/',
                                       headers=dict(Authorization=f'Bearer {auth_token}'))
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data.decode())
            self.assertEqual(len(response_data['data']), 3)
            # Update existing rating, number of records must be the same
            response = add_rating(self, 1, 3, 5, auth_token, API_VERSIONS[0])
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Rating updated.')
            response = self.client.get(f'/api/{API_VERSIONS[0]}/rating/',
                                       headers=dict(Authorization=f'Bearer {auth_token}'))
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data.decode())
            self.assertEqual(len(response_data['data']), 3)
            # Remove two ratings
            add_rating(self, 1, 2, None, auth_token, API_VERSIONS[0])
            add_rating(self, 1, 3, None, auth_token, API_VERSIONS[0])
            response = self.client.get(f'/api/{API_VERSIONS[0]}/rating/',
                                       headers=dict(Authorization=f'Bearer {auth_token}'))
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data.decode())
            self.assertEqual(len(response_data['data']), 1)

    def test_get_admin_service_no_auth(self):
        """
        Test for unauthorized admin requests
        """
        with self.client:
            login_data = register_and_login(self)  # Normal account
            auth_token = login_data['Authorization']
            response = self.client.get(f'/api/{API_VERSIONS[0]}/rating/',
                                       headers=dict(Authorization=f'Bearer {auth_token}'))
            self.assertEqual(response.status_code, 401)
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'admin token required')
