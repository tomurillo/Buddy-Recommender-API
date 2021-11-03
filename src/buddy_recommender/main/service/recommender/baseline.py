from .base import BuddyRecommender
from buddy_recommender.main.service.rating_service import get_item_average_rating


class BaselineRecommender(BuddyRecommender):
    """
    Baseline recommender: return global average score
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
        :return: predicted rating
        """
        return get_item_average_rating(item_id)
