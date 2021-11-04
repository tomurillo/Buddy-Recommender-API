from .memory_based import UserBasedCFRecommender
from buddy_recommender.main.model.exceptions import ResourceAlreadyExistsException


def rating_prediction(user_id: int, item_id: int, method='default'):
    """
    Perform a prediction for a numeric rating given by a user to an item
    :param user_id:
    :param item_id:
    :param method:
    :return:
    """
    if method == 'default':
        recommender = UserBasedCFRecommender(top_k=20)
    else:
        response_object = {
            'status': 'fail',
            'message': f'Recommender method "{method}" does not exist.',
        }
        return response_object, 404
    try:
        prediction = recommender.predict_rating(user_id, item_id)
        return {
            'user_id': user_id,
            'item_id': item_id,
            'predicted_rating': prediction,
        }
    except ResourceAlreadyExistsException:
        response_object = {
            'status': 'fail',
            'message': f'User {user_id} already rated item {item_id}.',
        }
        return response_object, 409
