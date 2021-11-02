import json

from buddy_recommender.test.base import BaseTestCase
from buddy_recommender.test.test_auth import admin_register_and_login
from buddy_recommender.test.test_rating import add_rating
from buddy_recommender.main.service.recommender.memory_based import UserBasedCFRecommender


class TestRecommendationBlueprint(BaseTestCase):
    def test_user_based_cf_recommend(self):
        """
        Test for user-based CF recommendations
        :return:
        """
        with self.client:
            # Create admin account and login
            login_data = admin_register_and_login(self)
            auth_token = login_data['Authorization']
            # Add a few ratings
            add_rating(self, 1, 1, 5, auth_token, 'v1')
            add_rating(self, 1, 3, 1, auth_token, 'v1')
            add_rating(self, 2, 1, 2, auth_token, 'v1')
            add_rating(self, 2, 2, 5, auth_token, 'v1')
            add_rating(self, 3, 1, 4, auth_token, 'v1')
            add_rating(self, 3, 3, 1, auth_token, 'v1')
            add_rating(self, 3, 2, 2, auth_token, 'v1')
            recommender = UserBasedCFRecommender(top_k=10)
            recommender.predict_rating(1, 2)
            self.assertTrue(True)


