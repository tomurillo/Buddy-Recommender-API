from math import ceil
from typing import List, Dict, Tuple
from operator import itemgetter
from itertools import islice

from buddy_recommender.main.service.rating_service import *
from buddy_recommender.main.model.exceptions import *


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

    def recommend(self, user_id: int, n: int) -> Dict[int, float]:
        """
        Given a user, recommend n items (not rated yet)
        :param user_id: numeric user ID
        :param n: number of items to recommend
        :return: dict<item id, (predicted rating, confidence)>, ordered by descending rating prediction
        """
        if n <= 0:
            n = 1
        user_items = np.array([r.item_id for r in get_user_ratings(user_id)], dtype=int)
        all_items = np.arange(1, get_maximum_item_id()+1, dtype=int)
        unrated_items = np.setdiff1d(all_items, user_items)
        predicted_ratings = {}
        for i in unrated_items:
            predicted_ratings[i] = self.predict_rating(user_id, int(i))
        sorted_predictions = {k: v for k, v in sorted(predicted_ratings.items(), key=itemgetter(1), reverse=True)}
        return dict(islice(sorted_predictions.items(), n))

    def predict_rating(self, user_id: int, item_id: int) -> Tuple[float, float]:
        """
        Perform a single prediction of a rating for a user and an item
        :param user_id: numeric user ID
        :param item_id: numeric item ID
        :return: (float, float): predicted score given by the user to the item and confidence of prediction
        """
        user_max = get_maximum_user_id()
        item_max = get_maximum_item_id()
        if 0 <= user_id <= user_max:
            if 0 <= item_id <= item_max:
                rating = get_rating(user_id, item_id)
            else:
                raise ItemDoesNotExistException(f'Item {item_id} does not exist!')
        else:
            raise UserDoesNotExistException(f'User {user_id} does not exist!')
        if not rating:
            return self._predict_rating(user_id, item_id)
        else:
            raise ResourceAlreadyExistsException(
                f'User {user_id} already rated item {item_id} with a score of {rating.rating}')

    def _predict_rating(self, user_id: int, item_id: int) -> Tuple[float, float]:
        """
        Subclass-specific method that will perform the prediction
        :param user_id: numeric user ID
        :param item_id: numeric item ID
        :return: (float, float): predicted score given by the user to the item and confidence of prediction
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
        if not force and self.user_item_matrix is not None and self.user_item_matrix.size > 0:
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
