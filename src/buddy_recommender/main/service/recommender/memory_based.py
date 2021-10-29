import numpy as np

from buddy_recommender.main.service.rating_service import fetch_ratings
from buddy_recommender.main.model.ratings import Rating


def user_based_cf_recommend(user_id, item_id):
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
    # Compute pearson's r between each user and the target user (according to ratings)
    for u in relevant_users:
        pass

    u_ids = []
    ratings_matrix = []
    for r in item_ratings:
        u_ids.append(r.user_id)
        ratings_matrix.append(r.rating)
    print(ratings_matrix)
    pearson_r = np.corrcoef(ratings_matrix)
    print(pearson_r)
