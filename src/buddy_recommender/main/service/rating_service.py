from sqlalchemy import func

from typing import Union

from buddy_recommender.main import db
from buddy_recommender.main.service.util import save_changes, delete_row
from buddy_recommender.main.model.ratings import Rating


def save_rating(data):
    try:
        row = Rating.query.filter_by(user_id=data['user_id'],
                                     item_id=data['item_id']).first()
        if row:
            if 'rating' in data:  # Update existing row
                row.rating = data['rating']
                msg = 'Rating updated.'
            else:  # Delete existing row
                delete_row(row)
                msg = 'Rating deleted.'
            save_changes()
            response_object = {
                'status': 'success',
                'message': msg
            }
            return response_object, 200
        else:  # Add new row
            new_row = Rating(
                user_id=data['user_id'],
                item_id=data['item_id'],
                rating=data['rating']
            )
            save_changes(new_row)
            response_object = {
                'status': 'success',
                'message': 'New rating added.'
            }
            return response_object, 201
    except KeyError:
        response_object = {
            'status': 'fail',
            'message': 'Missing required parameters.',
        }
        return response_object, 400


def fetch_ratings(user_id: Union[int, None], item_id: Union[int, None], columns=None):
    """
    Fetch ratings given a user and/or item
    :param user_id: Unique ID of an existing user; None to fetch all users
    :param item_id: Unique ID of an existing item; None to fetch all items
    :param columns: If not None, only the selected model columns will be fetched; otherwise, fetch whole rows
    :return: An array with rating instances
    """
    if user_id is not None and item_id is not None:
        ratings = get_rating(user_id, item_id)
    elif item_id is None:
        ratings = get_user_ratings(user_id, columns)
    elif user_id is None:
        ratings = get_item_ratings(item_id, columns)
    else:
        raise ValueError('Both user_id and item_id cannot be None!')
    return ratings


def get_rating(user_id, item_id):
    return Rating.query.filter_by(user_id=user_id, item_id=item_id).first()


def get_user_ratings(user_id, columns=None):
    if columns is None:
        columns = Rating
    return db.session.query(columns).filter_by(user_id=user_id).all()


def get_user_item_ratings(users=None, columns=None):
    if users is None:
        users = []
    if columns is None:
        columns = Rating
    return db.session.query(columns).filter(Rating.user_id.in_(users)).all()


def get_item_ratings(item_id, columns=None):
    if columns is None:
        columns = Rating
    return db.session.query(columns).filter_by(item_id=item_id).all()


def delete_rating(user_id, item_id):
    rows = Rating.query.filter_by(user_id=user_id, item_id=item_id).delete()
    if rows > 0:
        save_changes()
        response_object = {
            'status': 'success',
            'message': 'Rating deleted.'
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Rating does not exist.',
        }
        return response_object, 404


def get_maximum_value(column):
    max_row = db.session.query(Rating, func.max(column)).first()
    return max_row[1] if max_row else 0


def get_maximum_user_id():
    return get_maximum_value(Rating.user_id)


def get_maximum_item_id():
    return get_maximum_value(Rating.item_id)


def get_all_ratings():
    return Rating.query.all()
