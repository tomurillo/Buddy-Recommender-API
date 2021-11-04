import numpy as np

from .base import BuddyRecommender
from buddy_recommender.main.service.rating_service import fetch_ratings
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

    def _predict_rating(self, user_id: int, item_id: int) -> float:
        """
        Perform a single user-based CF recommendation
        :param user_id: numeric user ID
        :param item_id: numeric item ID
        :return: predicted score given by the user to the item
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
        # Subtract user's average score
        user_means = np.true_divide(self.user_item_matrix.sum(1), (self.user_item_matrix > 0.01).sum(1))
        score_deviations = np.subtract(self.user_item_matrix, user_means.reshape(-1, 1),
                                       where=self.user_item_matrix > 0.01)
        # Compute pearson's r between each user and the target user (according to ratings)
        correlations = np.corrcoef(self.user_item_matrix)[:, user_id-1]
        # Sort descending, select top-k, ignore target user
        sort_idx = np.argsort(correlations)[::-1][1: self.top_k+1]
        item_idx = item_id-1
        n_considered = 0
        for user_idx in sort_idx:
            if correlations[user_idx] <= 0:
                break
            predicted += score_deviations[user_idx, item_idx] * self.user_item_matrix[user_idx, item_idx]
            n_considered += 1
        if n_considered == 0:
            predicted = self.DEFAULT_SCORE
        else:
            predicted /= np.sum(correlations[sort_idx[:n_considered]])  # Score normalization
            predicted += user_means[user_id-1]  # Add target user average score
        return self._round_score_prediction(predicted)
