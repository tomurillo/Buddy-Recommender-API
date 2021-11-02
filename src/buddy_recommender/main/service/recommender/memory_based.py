import numpy as np

from .base import BuddyRecommender
from buddy_recommender.main.service.rating_service import fetch_ratings, get_user_item_ratings
from buddy_recommender.main.model.ratings import Rating


class UserBasedCFRecommender(BuddyRecommender):
    """
    Recommender based on User-based Collaborative Filtering
    """

    def __init__(self, top_k: int):
        """
        UserBasedCFRecommender constructor
        :param top_k: top k elements to use in similarity computations
        """
        super().__init__(top_k)

    def predict_rating(self, user_id, item_id):
        """
        Perform a single user-based CF recommendation
        :param user_id:
        :param item_id:
        :return:
        """
        # Fetch users that have rated target item
        relevant_users = [r.user_id for r in fetch_ratings(
            item_id=item_id,
            user_id=None,
            columns=Rating.user_id)]
        # Create user-item matrix for relevant users only
        self._create_user_item_matrix(users=relevant_users)
        # Compute pearson's r between each user and the target user (according to ratings)
        # correlations = np.corrcoef(self.user_item_matrix)

