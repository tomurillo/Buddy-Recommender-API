from .base import BuddyRecommender
from buddy_recommender.main.service.rating_service import get_item_average_rating


class BaselineRecommender(BuddyRecommender):
    """
    Baseline recommender: always returns average item score as rating prediction
    """

    def __init__(self, top_k: int):
        """
        UserBasedCFRecommender constructor
        :param top_k: top k elements to use in similarity computations
        """
        super().__init__(top_k)

    def _predict_rating(self, user_id, item_id):
        """
        Perform a simple user-item recommendation based on the average global rating of the item
        :param user_id: numeric user ID
        :param item_id: numeric item ID
        :return: predicted score for the item
        """
        return get_item_average_rating(item_id)
