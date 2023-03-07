from flask_login import UserMixin
from exts import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    authenticated = db.Column(db.Boolean, nullable=False, default=False)
