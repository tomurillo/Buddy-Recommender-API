import json

from buddy_recommender.test.base import BaseTestCase, API_VERSIONS
from buddy_recommender.test.test_auth import register_and_login
from buddy_recommender.test.test_rating import add_rating

from buddy_recommender.main.service.recommender.memory_based import UserBasedCFRecommender


def add_test_ratings(self, auth_token):
    """
    Add a bunch of user-item ratings to be used in tests
    :param self: TestCase instance
    :param auth_token: request authorization token
    :return: None; add ratings to DB
    """
    add_rating(self, 1, 1, 5, auth_token, 'v1')
    add_rating(self, 1, 3, 1, auth_token, 'v1')
    add_rating(self, 2, 1, 2, auth_token, 'v1')
    add_rating(self, 2, 2, 5, auth_token, 'v1')
    add_rating(self, 3, 1, 4, auth_token, 'v1')
    add_rating(self, 3, 3, 1, auth_token, 'v1')
    add_rating(self, 3, 2, 2, auth_token, 'v1')
    add_rating(self, 3, 4, 5, auth_token, 'v1')


class TestRecommendationBlueprint(BaseTestCase):
    def test_default_rating_prediction(self):
        """
        Test for user-based CF score prediction
        :return:
        """
        with self.client:
            # Create account and login, use account to create base user-item ratings
            login_data = register_and_login(self)
            auth_token = login_data['Authorization']
            add_test_ratings(self, auth_token)
            # Get prediction for user 1, item 2
            response = self.client.get(f'/api/{API_VERSIONS[0]}/prediction/user/1/item/2',
                                       headers=dict(Authorization=f'Bearer {auth_token}'))
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data.decode())
            self.assertEqual(response_data['data']['user_id'], 1)
            self.assertEqual(response_data['data']['item_id'], 2)
            self.assertTrue(response_data['data']['predicted_rating'] >= 1)
            self.assertTrue(response_data['data']['predicted_rating'] <= 5)

    def test_prediction_existing_rating(self):
        """
        Test for predicting an already existing user-item score
        :return:
        """
        with self.client:
            login_data = register_and_login(self)
            auth_token = login_data['Authorization']
            add_test_ratings(self, auth_token)
            # Get prediction for existing score
            response = self.client.get(f'/api/{API_VERSIONS[0]}/prediction/user/3/item/2',
                                       headers=dict(Authorization=f'Bearer {auth_token}'))
            self.assertEqual(response.status_code, 409)
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'User 3 already rated item 2.')

    def test_rating_prediction_no_auth(self):
        """
        Test for unauthorized requests
        """
        fake_auth_token = 'asdf123'
        with self.client:
            login_data = register_and_login(self)
            auth_token = login_data['Authorization']
            add_test_ratings(self, auth_token)
            response = self.client.get(f'/api/{API_VERSIONS[0]}/prediction/user/3/item/2')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'Provide a valid auth token.')
            response = self.client.get(f'/api/{API_VERSIONS[0]}/prediction/user/3/item/2',
                                       headers=dict(Authorization=f'Bearer {fake_auth_token}'))
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(response_data['status'] == 'fail')
            self.assertTrue(response_data['message'] == 'Invalid token. Please log in again.')

    def test_recommendation(self):
        """
        Test for item recommendations
        """
        with self.client:
            login_data = register_and_login(self)
            auth_token = login_data['Authorization']
            add_test_ratings(self, auth_token)
            # Get 1 recommendation for user 1
            response = self.client.get(f'/api/{API_VERSIONS[0]}/prediction/top/1/user/1',
                                       headers=dict(Authorization=f'Bearer {auth_token}'))
            self.assertEqual(response.status_code, 200)
            payload = json.loads(response.data.decode())['data']
            self.assertEqual(len(payload), 1)
            self.assertEqual(payload[0]['user_id'], 1)
            self.assertTrue(payload[0]['predicted_rating'] >= 1)
            self.assertTrue(payload[0]['predicted_rating'] <= 5)
            self.assertTrue(any(payload[0]['item_id'] == i for i in [2, 4]))
            # Get 2 recommendations for user 1
            response = self.client.get(f'/api/{API_VERSIONS[0]}/prediction/top/2/user/1',
                                       headers=dict(Authorization=f'Bearer {auth_token}'))
            self.assertEqual(response.status_code, 200)
            payload = json.loads(response.data.decode())['data']
            self.assertEqual(len(payload), 2)
            self.assertTrue(all(d['user_id'] == 1 for d in payload))
            self.assertTrue(all(d['predicted_rating'] >= 1 for d in payload))
            self.assertTrue(all(d['predicted_rating'] <= 5 for d in payload))
            self.assertTrue(all(d['item_id'] in [2, 4] for d in payload))
            self.assertEqual(len(list({d['item_id']: d for d in payload}.values())), 2)  # No duplicate items
