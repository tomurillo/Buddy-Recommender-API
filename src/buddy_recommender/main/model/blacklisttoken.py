from .. import db
from sqlalchemy.sql import func


class BlacklistToken(db.Model):
    """
    Token Model for storing blacklisted JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '<token-id: token: {}>'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token: str) -> bool:
        """
        Check whether the given auth token has been blacklisted
        :param auth_token: an auth token string
        :return: True if token has been blacklisted; False otherwise
        """
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        return bool(res)
