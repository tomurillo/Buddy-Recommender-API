from buddy_recommender.main import db


def save_changes(data=None):
    if data:
        db.session.add(data)
    db.session.commit()


def delete_row(row):
    db.session.delete(row)
