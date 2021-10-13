from .util import save_changes
from buddy_recommender.main.model.user import Account
from typing import Dict, Tuple


def save_new_account(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = Account.query.filter_by(email=data['email']).first()
    if not user:
        new_user = Account(
            email=data['email'],
            password=data['password'],
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Account already exists. Log in or use a different email address.',
        }
        return response_object, 409


def get_all_accounts():
    return Account.query.all()


def get_account(email):
    return Account.query.filter_by(email=email).first()


def generate_token(account: Account) -> Tuple[Dict[str, str], int]:
    try:
        auth_token = Account.encode_auth_token(account.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token
        }
        return response_object, 201
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'An error occurred. Please try again.'
        }
        return response_object, 401
