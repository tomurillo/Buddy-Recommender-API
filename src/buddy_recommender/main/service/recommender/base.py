from buddy_recommender.main.service.rating_service import get_user_ratings, get_item_ratings, \
    get_maximum_user_id, get_maximum_item_id

from typing import Union, List

import numpy as np


class BuddyRecommender(object):
    """
    Base class for recommending items to users.
    """

    target_user = -1
    user_item_matrix = None

    def __init__(self, top_k: int):
        """
        BuddyRecommender base constructor
        :param top_k: top k elements to use in similarity computations
        :return:
        """
        self.top_k = top_k

    def predict_rating(self, user_id, item_id):
        raise NotImplementedError()

    def _create_user_item_matrix(self, users: Union[List, None] = None):
        """
        Create a NumPy array (user-item matrix) given users or items
        :param users: List of relevant user ids
        :return: None, store user-item matrix in user_item_matrix instance attribute
        """
        max_user = get_maximum_user_id()
        max_item = get_maximum_item_id()
        ret_matrix = np.zeros((max_user, max_item))
        if users:
            for u in users:
                for r in get_user_ratings(u):
                    ret_matrix[u-1, r.item_id-1] = r.rating
        self.user_item_matrix = ret_matrix
