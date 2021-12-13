from flask import request
from flask_restx import Resource
from typing import Dict, Tuple

from ..util.dto import AccountDto
from ..util.decorator import admin_token_required
from ..service.account_service import get_all_accounts, save_new_account, get_account


api = AccountDto.api
_account = AccountDto.user


@api.route('/')
class AccountList(Resource):
    @api.doc('List of accounts that have API access')
    @admin_token_required
    @api.marshal_list_with(_account, envelope='data')
    def get(self):
        return get_all_accounts()

    @api.expect(_account, validate=True)
    @api.response(201, 'Account successfully added.')
    @api.doc('Add a new API user account')
    @admin_token_required
    def post(self) -> Tuple[Dict[str, str], int]:
        return save_new_account(data=request.json)


@api.route('/<email>')
@api.param('email', 'The email address of the account')
@api.response(404, 'Account not found.')
class Account(Resource):
    @api.doc('get an account by email')
    @admin_token_required
    @api.marshal_with(_account)
    def get(self, email):
        user = get_account(email)
        if not user:
            api.abort(404)
        else:
            return user
