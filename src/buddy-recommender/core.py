# -*- coding: utf-8 -*-
"""
    buddy-recommender.core
    ~~~~~~~~~~~~~
    Core module
"""

from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

# Flask-SQLAlchemy extension instance
db = SQLAlchemy()

# Basic auth support
auth = HTTPBasicAuth()


class BuddyError(Exception):
    """
    Base application error class.
    """
    def __init__(self, msg):
        self.msg = msg

