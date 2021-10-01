import os

from flask_migrate import Migrate

from buddy_recommender.main import create_app, db
from buddy_recommender.main.model import ratings

app = create_app(os.getenv('BOILERPLATE_ENV') or None)

app.app_context().push()

migrate = Migrate(app, db)


@app.route('/')
def home():
    return {
        'message': 'Buddy Recommender RESTful API'
    }, 200


if __name__ == '__main__':
    app.run()
