from flask import Flask

from exts import db, bcrypt, login_manager
from models.user_model import User
from controllers import api
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'lkghIUG80yIUOtyIIN07giyOIFG78'

CORS(app)

db.init_app(app)

migrate = Migrate(app, db)

bcrypt.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'user_login'

api.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# @app.route('/migrate')
# def migrate():
#     with app.app_context():
#         db.create_all()
#         print("migrated")
#         return "migrated"


if __name__ == '__main__':
    app.run(debug=True)
