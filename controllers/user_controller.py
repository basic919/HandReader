from flask_restx import Namespace, Resource
from services.user_service import *
from flask import request
from models.user_model import token_required


api = Namespace('user', description="A namespace for User")


@api.route('/login')
class Login(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        return login_user(json_data)


@api.route('/permission')
class Permission(Resource):
    @token_required
    def get(self):
        return jsonify({"value": True,
                        "message": "Logged in"})


@api.route('/register')
class Register(Resource):
    def post(self):
        return register_user(request.json['address'], request.json['password'])


@api.route('/confirm_email')
class ConfirmEmail(Resource):
    def get(self):
        return confirm_email(request.args.get('token'))


@api.route('/forgot_password')
class ForgotPassword(Resource):
    def post(self):
        return forgot_password(request.json['address'])


@api.route('/new_password')
class NewPassword(Resource):
    def post(self):
        return set_new_password(request.args.get('token'), request.json['new_password'])
