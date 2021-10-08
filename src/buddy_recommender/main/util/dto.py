from flask_restx import Namespace, fields


class RatingDto:
    api = Namespace('rating', description='User-item ratings related operations')
    rating = api.model('rating', {
        'user_id': fields.Integer(required=True, description='id of user rating the item'),
        'item_id': fields.Integer(required=True, description='id of item being rated by user'),
        'rating': fields.Integer(description='Numeric rating given by user to item'),
        'created': fields.DateTime(dt_format='rfc822', readonly=True),
        'updated': fields.DateTime(dt_format='rfc822', readonly=True),
    })
