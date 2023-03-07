from flask import Flask, render_template
from config import Config
from exts import db, bcrypt, login_manager, mail
from models.user_model import User
from models.password_reset_model import PasswordReset
from controllers import api
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

api.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)
