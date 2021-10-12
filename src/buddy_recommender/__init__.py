from flask_restx import Api
from flask import Blueprint

from .main.controller.api.v1.rating_controller import api as rating_v1_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='BUDDY RECOMMENDER API',
    version='1.0',
    description='a web service for personalized AT recommendations based on collaborative filtering methods',
)

api.add_namespace(rating_v1_ns, path='/api/v1/rating')
