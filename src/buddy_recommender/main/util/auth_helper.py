from buddy_recommender.main.model.user import Account
from buddy_recommender.main.service.blacklist_service import save_token
from typing import Dict, Tuple


class Auth:

    @staticmethod
    def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        try:
            user = Account.query.filter_by(email=data.get('email')).first()
            if not user:
                msg = 'email does not exist'
            elif not user.check_password(data.get('password')):
                msg = 'wrong password'
            else:
                auth_token = Account.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token
                    }
                    return response_object, 200
                else:
                    msg = 'error encoding auth token'
            response_object = {
                'status': 'fail',
                'message': msg,
            }
            return response_object, 401
        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data: str) -> Tuple[Dict[str, str], int]:
        auth_token = data.split(" ")[1] if data else ''
        if auth_token:
            response_msg = Account.decode_auth_token(auth_token)
            if not isinstance(response_msg, str):
                # mark the token as blacklisted (token can't be used again after logging out)
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': response_msg
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_header = new_request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1] if auth_header else ''
        if auth_token:
            resp = Account.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = Account.query.filter_by(id=resp).first()
                if not user:
                    resp = 'account does not exist.'
                else:
                    response_object = {
                        'status': 'success',
                        'data': {
                            'user_id': user.id,
                            'email': user.email,
                            'admin': user.admin,
                            'registered_on': str(user.created)
                        }
                    }
                    return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
