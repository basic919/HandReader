from flask import Flask, render_template
from config import Config
from exts import db, bcrypt, mail
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
mail.init_app(app)

api.init_app(app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
