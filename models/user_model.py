from exts import db
from functools import wraps
from flask import request, jsonify
import jwt
from config import Config


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    authenticated = db.Column(db.Boolean, nullable=False, default=False)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({"value": False,
                            'message': 'A valid token is missing.'})
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            user = User.query.filter_by(address=data['address']).first()
            if not user:
                return jsonify({"value": False,
                                'message': 'No such user.'})
            if not user.authenticated:
                return jsonify({"value": False,
                                'message': 'User is not authenticated.'})
        except:
            return jsonify({"value": False,
                            'message': 'Token is invalid.'})

        return f(*args, **kwargs)

    return decorator
