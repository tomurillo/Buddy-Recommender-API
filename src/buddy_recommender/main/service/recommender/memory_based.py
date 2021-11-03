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
        predicted = 0.0
        # Fetch users that have rated target item
        relevant_users = [r.user_id for r in fetch_ratings(
            item_id=item_id,
            user_id=None,
            columns=Rating.user_id)]
        relevant_users.append(user_id)
        # Create user-item matrix for relevant users only
        self._create_user_item_matrix(users=relevant_users)
        # Compute pearson's r between each user and the target user (according to ratings)
        correlations = np.corrcoef(self.user_item_matrix)[:, user_id-1]
        # Sort descending, select top-k, ignore target user
        sort_idx = np.argsort(correlations)[::-1][1: self.top_k+1]
        item_idx = item_id-1
        n_considered = 0
        for user_idx in sort_idx:
            if correlations[user_idx] <= 0:
                break
            predicted += correlations[user_idx] * self.user_item_matrix[user_idx, item_idx]
            n_considered += 1
        if n_considered == 0:
            predicted = self.DEFAULT_SCORE
        return self._round_score_prediction(predicted)
