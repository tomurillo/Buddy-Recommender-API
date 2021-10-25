import json

from buddy_recommender.test.base import BaseTestCase
from buddy_recommender.test.test_auth import create_account_and_validate

API_VERSIONS = ['v1']


def add_rating(self, user_id, item_id, rating, auth_token, api_version):
    return self.client.post(
        f'/api/{api_version}/rating/',
        data=json.dumps({
            'user_id': user_id,
            'item_id': item_id,
            'rating': rating,
        }),
        headers=dict(Authorization=f'Bearer {auth_token}'),
        content_type='application/json'
    )


class TestRatingBlueprint(BaseTestCase):
    def test_add_rating(self):
        """
        Test for adding a new rating
        """
        with self.client:
            login_data = create_account_and_validate(self)
            auth_token = login_data['Authorization']
            for api in API_VERSIONS:
                # Add new rating
                response = add_rating(self, 1, 2, 5, auth_token, api)
                response_data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertTrue(response_data['status'] == 'success')
                self.assertTrue(response_data['message'] == 'New rating added.')
                # Retrieve added rating
                response = self.client.get(f'/api/{api}/rating/user/1/item/2',
                                           headers=dict(Authorization=f'Bearer {auth_token}'))
                response_data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response_data['data']['user_id'], 1)
                self.assertEqual(response_data['data']['item_id'], 2)
                self.assertEqual(response_data['data']['rating'], 5)
                self.assertTrue(response_data['data']['created'])
                self.assertTrue(response_data['data']['updated'])
                # Same request, change parameter order
                response = self.client.get(f'/api/{api}/rating/item/2/user/1',
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
            login_data = create_account_and_validate(self)
            auth_token = login_data['Authorization']
            for api in API_VERSIONS:
                # Add new rating
                response = add_rating(self, 1, 2, 5, auth_token, api)
                self.assertEqual(response.status_code, 201)
                # Request rating not in database
                response = self.client.get(f'/api/{api}/rating/user/1/item/3',
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
            create_account_and_validate(self)
            for api in API_VERSIONS:
                # No token
                response = add_rating(self, 1, 2, 5, None, api)
                response_data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 401)
                self.assertTrue(response_data['status'] == 'fail')
                self.assertTrue(response_data['message'] == 'Invalid token. Please log in again.')
                # Invalid token
                response = add_rating(self, 1, 2, 5, fake_auth_token, api)
                response_data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 401)
                self.assertTrue(response_data['status'] == 'fail')
                self.assertTrue(response_data['message'] == 'Invalid token. Please log in again.')
