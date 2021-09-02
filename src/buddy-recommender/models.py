# -*- coding: utf-8 -*-
"""
    buddy-recommender.models
    ~~~~~~~~~~~~~~~
    Consolidated models module
"""

from core import db
from helpers import JsonSerializer
from datetime import datetime


class Rating(JsonSerializer, db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer(), primary_key=True)
    uid = db.Column(db.Integer(), nullable=False)  # User ID
    pid = db.Column(db.Integer(), nullable=False)  # Product ID
    score = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}, Product {}>: {} points'.format(self.uid, self.pid, self.score)
