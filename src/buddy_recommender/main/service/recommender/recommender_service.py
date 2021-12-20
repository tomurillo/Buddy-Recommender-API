from .memory_based import UserBasedCFRecommender
from buddy_recommender.main.model.exceptions import ResourceAlreadyExistsException, UserDoesNotExistException


def recommendation_predictions(user_id: int, n_items: int, method='default'):
    """
    Predict n_items item recommendations for the given user following a recommendation strategy
    :param user_id: numeric user ID
    :param n_items: number of items to be recommended
    :param method: recommendation method to employ
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
        recommendations = recommender.recommend(user_id, n_items)
    except UserDoesNotExistException as e:
        response_object = {
            'status': 'fail',
            'message': str(e),
        }
        return response_object, 404
    return [
        {
            'user_id': user_id,
            'item_id': i,
            'predicted_rating': r,
            'confidence': c
        }
        for i, (r, c) in recommendations.items()]


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
        prediction, confidence = recommender.predict_rating(user_id, item_id)
        return {
            'user_id': user_id,
            'item_id': item_id,
            'predicted_rating': prediction,
            'confidence': confidence,
        }
    except ResourceAlreadyExistsException:
        response_object = {
            'status': 'fail',
            'message': f'User {user_id} already rated item {item_id}.',
        }
        return response_object, 409
