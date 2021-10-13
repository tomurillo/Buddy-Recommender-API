from flask import request
from flask_restx import Resource

from buddy_recommender.main.util.auth_helper import Auth
from ..util.dto import AuthDto
from typing import Dict, Tuple

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
    Account Login Resource
    """
    @api.doc('log in with an existing account')
    @api.expect(user_auth, validate=True)
    def post(self) -> Tuple[Dict[str, str], int]:
        return Auth.login_user(data=request.json)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Account Logout Resource
    """
    @api.doc('logout an account')
    def post(self) -> Tuple[Dict[str, str], int]:
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
