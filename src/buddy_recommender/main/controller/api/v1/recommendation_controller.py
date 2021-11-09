from flask_restx import Resource

from buddy_recommender.main.util.dto import PredictionDto
from buddy_recommender.main.util.decorator import token_required
from buddy_recommender.main.service.recommender.recommender_service import *

api = PredictionDto.api
_prediction = PredictionDto.prediction


@api.route('/top/<int:k_items>/user/<int:user_id>')
@api.param('k_items', 'Number of items to return')
@api.param('user_id', 'User identifier')
class RecommendItems(Resource):
    @api.doc('recommend items to a user that he/she has not rated yet')
    @token_required
    @api.marshal_list_with(_prediction, envelope='data')
    def get(self, k_items, user_id):
        """
        recommend items to a user that he/she has not rated yet
        """
        result = recommendation_predictions(user_id, k_items, method='default')
        if type(result) == tuple:
            api.abort(result[1], status=result[0]['status'], message=result[0]['message'])
        else:
            return result


@api.route('/user/<int:user_id>/item/<int:item_id>')
@api.route('/item/<int:item_id>/user/<int:user_id>')
@api.param('user_id', 'User identifier')
@api.param('item_id', 'Item (AT entry) identifier')
class UserItemRatingPrediction(Resource):
    @api.doc('perform a default rating score prediction for a user-item pair')
    @token_required
    @api.marshal_with(_prediction, envelope='data')
    def get(self, user_id, item_id):
        """
        perform a default rating score prediction for a user-item pair
        """
        result = rating_prediction(user_id, item_id, method='default')
        if type(result) == tuple:
            api.abort(result[1], status=result[0]['status'], message=result[0]['message'])
        else:
            return result
