from buddy_recommender.main import db


def save_changes(data=None):
    if data:
        db.session.add(data)
    db.session.commit()


def delete_row(row):
    db.session.delete(row)


def get_or_create(model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        save_changes(instance)
        return instance
