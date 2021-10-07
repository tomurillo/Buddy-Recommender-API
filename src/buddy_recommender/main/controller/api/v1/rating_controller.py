from flask import request
from flask_restx import Resource

from buddy_recommender.main.util.dto import RatingDto
from buddy_recommender.main.service.rating_service import *

api = RatingDto.api
_rating = RatingDto.rating


@api.route('/')
class RatingList(Resource):
    @api.doc('list of user-item ratings')
    @api.marshal_list_with(_rating, envelope='data')
    def get(self):
        """
        List all user-item ratings
        """
        return get_all_ratings()

    @api.expect(_rating, validate=True)
    @api.response(201, 'Rating successfully added')
    @api.doc('add a new rating or update an existing rating')
    def post(self):
        """
        Create a new User-Item rating or update an existing one
        """
        data = request.json
        return save_rating(data=data)


@api.route('/user/<int:user_id>')
@api.param('user_id', 'User identifier')
@api.response(404, 'User not found.')
class UserRatingList(Resource):
    @api.doc('get all item ratings for a user')
    @api.marshal_list_with(_rating, envelope='data')
    def get(self, user_id):
        """
        get all item ratings for a user given its uid
        """
        ratings = get_user_ratings(user_id)
        if not ratings:
            api.abort(404)
        else:
            return ratings


@api.route('/item/<int:item_id>')
@api.param('item_id', 'Item identifier')
@api.response(404, 'Item not found.')
class ItemRatingList(Resource):
    @api.doc('get all user ratings for an item')
    @api.marshal_list_with(_rating, envelope='data')
    def get(self, item_id):
        """
        get all user ratings for an item give its item id
        """
        ratings = get_item_ratings(item_id)
        if not ratings:
            api.abort(404)
        else:
            return ratings


@api.route('/user/<int:user_id>/item/<int:item_id>')
@api.route('/item/<int:item_id>/user/<int:user_id>')
@api.param('user_id', 'User identifier')
@api.param('item_id', 'Item identifier')
@api.response(404, 'Rating not found.')
class UserItemRating(Resource):
    @api.doc('get the rating of a given user for a given item')
    @api.marshal_with(_rating, envelope='data')
    def get(self, user_id, item_id):
        """
        get all user ratings for an item give its item id
        """
        rating = get_rating(user_id, item_id)
        if rating:
            api.abort(404)
        else:
            return rating
