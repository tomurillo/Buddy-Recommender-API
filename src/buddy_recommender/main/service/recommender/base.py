from math import ceil
from typing import List

from buddy_recommender.main.service.rating_service import *
from buddy_recommender.main.model.exceptions import ResourceAlreadyExistsException


class BuddyRecommender(object):
    """
    Base class for recommending items to users.
    """

    DEFAULT_SCORE = 2.5

    target_user = -1
    user_item_matrix = None

    def __init__(self, top_k: int):
        """
        BuddyRecommender base constructor
        :param top_k: top k elements to use in similarity computations
        :return:
        """
        self.top_k = top_k

    def predict_rating(self, user_id: int, item_id: int) -> float:
        """
        Perform a single prediction of a rating for a user and an item
        :param user_id: numeric user ID
        :param item_id: numeric item ID
        :return: predicted score given by the user to the item
        """
        rating = get_rating(user_id, item_id)
        if not rating:
            return self._predict_rating(user_id, item_id)
        else:
            raise ResourceAlreadyExistsException(
                f'User {user_id} already rated item {item_id} with a score of {rating.rating}')

    def _predict_rating(self, user_id: int, item_id: int) -> float:
        """
        Subclass-specific method that will perform the prediction
        :param user_id: numeric user ID
        :param item_id: numeric item ID
        :return: predicted score given by the user to the item
        """
        raise NotImplementedError()

    def _create_user_item_matrix(self, users: Union[List, None] = None, force: bool = False):
        """
        Create a NumPy array (user-item matrix) given users or items
        :param users: List of relevant user ids
        :param force: Whether to force re-generation of the user-item matrix if it already exists in this instance
        :return: None, store user-item matrix in user_item_matrix instance attribute
        """
        if self.user_item_matrix and not force:
            return
        max_user = get_maximum_user_id()
        max_item = get_maximum_item_id()
        ret_matrix = np.zeros((max_user, max_item))
        for u in users:
            for r in get_user_ratings(u):
                ret_matrix[u-1, r.item_id-1] = r.rating
        self.user_item_matrix = ret_matrix

    def _create_full_user_item_matrix(self, force: bool = False):
        """
        Create the full user-item rating matrix (very memory demanding!)
        :param force: Whether to force re-generation of the user-item matrix if it already exists in this instance
        :return: None, store user-item matrix in user_item_matrix instance attribute
        """
        if self.user_item_matrix and not force:
            return
        ratings = get_all_ratings()
        max_user = get_maximum_user_id()
        max_item = get_maximum_item_id()
        ret_matrix = np.zeros((max_user, max_item))
        for r in ratings:
            ret_matrix[r.user_id - 1, r.item_id - 1] = r.rating
        self.user_item_matrix = ret_matrix

    @staticmethod
    def _round_score_prediction(score_prediction):
        return np.clip(ceil(score_prediction * 2) / 2, 1, 5)  # Round up to nearest 0.5
