from flask_restx import Namespace, fields


class RatingDto:
    api = Namespace('rating', description='User-item ratings related operations')
    rating = api.model('rating', {
        'user': fields.Integer(required=True, description='id of user rating the item'),
        'item': fields.Integer(required=True, description='id of item being rated by user'),
        'rating': fields.Integer(description='Numeric rating given by user to item'),
        'updated': fields.DateTime(dt_format='rfc822'),
    })

