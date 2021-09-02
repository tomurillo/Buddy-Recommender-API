# -*- coding: utf-8 -*-
"""
    buddy-recommender.core
    ~~~~~~~~~~~~~
    Core module
"""

from flask_sqlalchemy import SQLAlchemy
from flask_security import Security

# Flask-SQLAlchemy extension instance
db = SQLAlchemy()

# Flask-Security extension instance
security = Security()


class BuddyError(Exception):
    """
    Base application error class.
    """
    def __init__(self, msg):
        self.msg = msg

