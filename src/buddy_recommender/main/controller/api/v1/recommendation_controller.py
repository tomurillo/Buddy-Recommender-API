from flask_restx import Resource

from buddy_recommender.main.util.dto import PredictionDto
from buddy_recommender.main.util.decorator import token_required
from buddy_recommender.main.service.recommender.recommender_service import rating_prediction

api = PredictionDto.api
_prediction = PredictionDto.prediction


@api.route('predict/user/<int:user_id>/item/<int:item_id>')
@api.route('predict/item/<int:item_id>/user/<int:user_id>')
@api.param('user_id', 'User identifier')
@api.param('item_id', 'Item (AT entry) identifier')
class UserItemRatingPrediction(Resource):
    @api.doc('perform a default rating score prediction for a user-item pair')
    @token_required
    @api.marshal_with(_prediction, envelope='data')
    def get(self, user_id, item_id):
        """
        get all user ratings for an item given its item id
        """
        rating = rating_prediction(user_id, item_id, method='default')
        if rating:
            return rating
        else:
            api.abort(404, status="fail", message=f"Could not predict rating for user {user_id} and item {item_id}.")
