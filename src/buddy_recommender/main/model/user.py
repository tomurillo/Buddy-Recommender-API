import datetime
import jwt

from typing import Union

from .. import db, flask_bcrypt
from buddy_recommender.main.model.blacklisttoken import BlacklistToken
from ..config import key as app_secret_key
from sqlalchemy.sql import func


class Account(db.Model):
    """
    Account Model for storing user accounts that have access to the API
    """
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    admin = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(100))

    @property
    def password(self):
        raise AttributeError('Password is write-only')

    @password.setter
    def password(self, password: str):
        """
        Safely store the user' password
        :param password: password in plain text
        :return: None; password is hashed and stored
        """
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """
        Check whether the given password matches the user's password
        :param password: password to check against the user's
        :return: True if both passwords match; False otherwise
        """
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(account_id: int) -> bytes:
        """
        Generates the Auth Token
        :return: string
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': account_id
        }
        return jwt.encode(
            payload,
            app_secret_key,
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[str, int]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app_secret_key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return f"<uid {self.id}>"

    def __str__(self):
        return f"User <id={self.id}; email={self.email}; admin={self.admin}>"
