from .. import db
from sqlalchemy.sql import func


class Rating(db.Model):
    """
    Ratings model for storing main user-item rating matrix
    """

    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_id = db.Column(db.Integer, primary_key=True, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __str__(self):
        return f'<u: {self.user_id}, i: {self.item_id}>: score is {self.rating}'

    def __repr__(self):
        return f'<{self.user_id},{self.item_id}'
