import itsdangerous
from flask_restx import Namespace, Resource
from flask import render_template, make_response, request
from flask_login import login_user, login_required, logout_user
from exts import db, bcrypt, mail
from models.user_model import User
from models.password_reset_model import PasswordReset
from models.user_confirmation_model import UserConfirmation
from config import Config
from flask_mail import Message


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
        # json_data = request.get_json(force=True)
        email = request.json['address']
        password = request.json['password']
        if email:
            existing_user_address = User.query.filter_by(address=email).first()
            if existing_user_address:
                return False, 'That E-Mail address already exists. Please choose a different one.'

            serializer = itsdangerous.URLSafeTimedSerializer(Config.SECRET_KEY)
            token = serializer.dumps(email, salt='user-confirmation')

            hashed_password = bcrypt.generate_password_hash(password)
            new_user = User(address=json_data.get("address"), password=hashed_password)  # type: ignore
            db.session.add(new_user)

            # new_confirmation = UserConfirmation(address=json_data.get("address"), token=token)
            # db.session.add(new_confirmation)

            db.session.commit()

            msg = Message('HandReader - Reset Password Request', sender=Config.MAIL_SENDER_ADDRESS,
                          recipients=email)
            msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works\n\n" + token
            mail.send(msg)

            return True, "Registered"
        return False, "Something went wrong."


@api.route('/confirm_email')
class ConfirmEmail(Resource):
    def get(self):
        token = request.args.get('token')
        # Verify the token to ensure that it's valid and retrieve the user's email address
        serializer = itsdangerous.URLSafeTimedSerializer(Config.SECRET_KEY)
        try:
            email = serializer.loads(token, salt='user-confirmation', max_age=86400)
        except itsdangerous.SignatureExpired:
            return False, 'Confirmation link has expired.'
        except itsdangerous.BadSignature:
            return False, 'Invalid confirmation link.'

        # Mark the user's email as confirmed in the database

        user = User.query.filter_by(address=email).first()
        user.authenticated = True
        db.session.commit()

        return True, 'Email confirmed!'


@api.route('/forgot_password')
class ForgotPassword(Resource):
    def post(self):
        email = request.json['address']

        existing_reset_address = PasswordReset.query.filter_by(address=email).first()
        if existing_reset_address:
            return False, 'That E-Mail address already has a pending reset request. Please check your mail.'

        # Generate a secure token for the user
        serializer = itsdangerous.URLSafeTimedSerializer(Config.SECRET_KEY)
        token = serializer.dumps(email, salt='password-reset')

        # Store the token in a database or other persistent storage
        new_reset = PasswordReset(address=email, token=token)
        db.session.add(new_reset)
        db.session.commit()

        # Send an email to the user with a link to the password reset form
        msg = Message('HandReader: Reset Password Request', sender=Config.MAIL_SENDER_ADDRESS, recipients=[email])
        msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works\n\n" + token
        mail.send(msg)

        return True, 'Password reset email sent!'


@api.route('/new_password')
class NewPassword(Resource):
    def post(self):
        token = request.args.get('token')
        new_hashed_password = bcrypt.generate_password_hash(request.json['new_password'])

        serializer = itsdangerous.URLSafeTimedSerializer(Config.SECRET_KEY)
        try:
            email = serializer.loads(token, salt='password-reset', max_age=3600)
        except itsdangerous.SignatureExpired:
            return False, 'Password reset link has expired.'
        except itsdangerous.BadSignature:
            return False, 'Invalid reset link.'

        user = User.query.filter_by(address=email).first()
        user.password = new_hashed_password

        db.session.delete(PasswordReset.query.filter_by(token=token).first())

        db.session.commit()

        return True, "New password set successfully."
