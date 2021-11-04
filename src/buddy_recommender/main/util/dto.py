from flask_restx import Namespace, fields


class PredictionDto:
    api = Namespace('prediction', description='User-item rating prediction related operations')
    prediction = api.model('prediction', {
        'user_id': fields.Integer(required=True, description='id of user'),
        'item_id': fields.Integer(required=True, description='id of item'),
        'predicted_rating': fields.Float(description='Numeric rating predicted for this item for the user'),
    })


class RatingDto:
    api = Namespace('rating', description='User-item ratings related operations')
    rating = api.model('rating', {
        'user_id': fields.Integer(required=True, description='id of user rating the item'),
        'item_id': fields.Integer(required=True, description='id of item being rated by user'),
        'rating': fields.Integer(description='Numeric rating given by user to item'),
        'created': fields.DateTime(dt_format='rfc822', readonly=True),
        'updated': fields.DateTime(dt_format='rfc822', readonly=True),
    })


class AccountDto:
    api = Namespace('account', description='account related operations')
    user = api.model('account', {
        'email': fields.String(required=True, description='account email address'),
        'password': fields.String(required=True, description='account password'),
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='account email address'),
        'password': fields.String(required=True, description='account password'),
    })
