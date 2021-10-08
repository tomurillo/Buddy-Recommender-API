from buddy_recommender.main import db
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
                db.session.delete(row)
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


def get_rating(user_id, item_id):
    return Rating.query.filter_by(user_id=user_id, item_id=item_id).first()


def get_user_ratings(user_id):
    return Rating.query.filter_by(user_id=user_id).all()


def get_item_ratings(item_id):
    return Rating.query.filter_by(item_id=item_id).all()


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


def get_all_ratings():
    return Rating.query.all()


def save_changes(data=None):
    if data:
        db.session.add(data)
    db.session.commit()
