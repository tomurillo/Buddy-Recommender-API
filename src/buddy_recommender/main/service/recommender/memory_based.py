from typing import Tuple

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

    def _predict_rating(self, user_id: int, item_id: int) -> Tuple[float, float]:
        """
        Perform a single user-based CF recommendation
        :param user_id: numeric user ID
        :param item_id: numeric item ID
        :return: (float, float): predicted score given by the user to the item, confidence score of prediction
        """
        predicted = 0.0
        confidence = 0.0
        # Fetch users that have rated target item
        relevant_users = [r.user_id for r in fetch_ratings(
            item_id=item_id,
            user_id=None,
            columns=Rating.user_id)]
        if not relevant_users:
            return self.DEFAULT_SCORE, confidence
        # Create user-item matrix for relevant users only (skip for now)
        # relevant_users.append(user_id)
        # self._create_user_item_matrix(users=relevant_users, force=True)
        self._create_full_user_item_matrix()
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
        sum_corr = 0
        for user_idx in sort_idx:
            c = correlations[user_idx]
            if np.isnan(c) or c <= 0:
                continue
            predicted += score_deviations[user_idx, item_idx] * self.user_item_matrix[user_idx, item_idx]
            n_considered += 1
            sum_corr += c
        if n_considered == 0:
            predicted = self.DEFAULT_SCORE, 0.0
        else:
            confidence = min(n_considered, 100) / 100.0
            predicted /= sum_corr  # Score normalization
            predicted += user_means[user_id-1]  # Add target user average score
        return self._round_score_prediction(predicted), confidence
