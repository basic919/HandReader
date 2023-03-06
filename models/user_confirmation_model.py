from exts import db


class UserConfirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(40), nullable=False, unique=True)
    token = db.Column(db.String(), nullable=False)
    # Date tag can be added for extra security

