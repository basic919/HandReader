import itsdangerous
from flask_restx import Namespace, Resource
from flask import render_template, make_response, request
from flask_login import login_user, login_required, logout_user
from exts import db, bcrypt
from models.user_model import User
from models.password_resets import PasswordReset
from config import Config


api = Namespace('user', description="A namespace for User")


# data_sources_model = api.model(
#     "Users",
#     {
#         "id": fields.Integer(),
#         "address": fields.String(),
#         "password": fields.String(),
#         "authenticated": fields.Boolean(),
#     }
# )


@api.route('/home')
class HomeController(Resource):
    def get(self):
        return make_response(render_template('home.html'))



@api.route('/login')
class Login(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        if json_data:
            user = User.query.filter_by(address=json_data.get("address")).first()
            if user:
                if bcrypt.check_password_hash(user.password, json_data.get("password")):
                    login_user(user)
                    return True, "Logged in"
        return False, "Wrong E-Mail or address"


# @api.route('/dashboard')
# class Dashboard(Resource):
#     @login_required
#     def get(self):
#         return make_response(render_template('dashboard.html'))
@api.route('/dashboard')
class Dashboard(Resource):
    @login_required
    def get(self):
        return True


# @api.route('/logout')
# class Logout(Resource):
#     @login_required
#     def get(self):
#         logout_user()
#         return redirect(url_for('user_dashboard'))

@api.route('/logout')
class Logout(Resource):     # TODO: Finish this
    @login_required
    def get(self):
        logout_user()
        return True


@api.route('/register')
class Register(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if json_data:
            existing_user_address = User.query.filter_by(address=json_data.get("address")).first()
            if existing_user_address:
                return False, 'That E-Mail address already exists. Please choose a different one.'

            hashed_password = bcrypt.generate_password_hash(json_data.get("password"))
            new_user = User(address=json_data.get("address"), password=hashed_password)  # type: ignore
            db.session.add(new_user)
            db.session.commit()
            return True, "Registered"
        return False, "Something went wrong."

@api.route('/forgot_password')
class ForgotPassword(Resource):
    def post(self):
        email = request.json['email']

        existing_reset_address = PasswordReset.query.filter_by(address=email).first()
        if existing_reset_address:
            return False, 'That E-Mail address already has a pending reset request. Please check your mail.'

        # Generate a secure token for the user
        serializer = itsdangerous.URLSafeTimedSerializer(Config.SECRET_KEY)
        token = serializer.dumps(email, salt='password-reset')

        # Store the token in a database or other persistent storage
        # ...
        new_reset = PasswordReset(address=email, token=token)
        db.session.add(new_reset)
        db.session.commit()

        # Send an email to the user with a link to the password reset form
        # ...

        return 'Password reset email sent!'

@api.route('/new_password')
class Register(Resource):
    def post(self):
        token = request.args.get('token')
        new_hashed_password = bcrypt.generate_password_hash(request.json['new_password'])

        existing_reset = PasswordReset.query.filter_by(token=token).first()
        if not existing_reset:
            return False, 'No such reset request.'

        user = User.query.filter_by(address=existing_reset.address).first()
        user.password = new_hashed_password
        db.session.commit()
