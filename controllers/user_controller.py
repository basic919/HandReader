import itsdangerous
import jwt
from flask_restx import Namespace, Resource
from flask import request, url_for, jsonify
from exts import db, bcrypt, mail
from models.user_model import User, token_required
from models.password_reset_model import PasswordReset
from config import Config
from flask_mail import Message
import datetime


api = Namespace('user', description="A namespace for User")


@api.route('/login')
class Login(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        if json_data:
            user = User.query.filter_by(address=json_data.get("address")).first()
            if user:
                if bcrypt.check_password_hash(user.password, json_data.get("password")):
                    # login_user(user)
                    token = jwt.encode({'address': json_data.get("address"),
                                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
                                       Config.SECRET_KEY, "HS256")

                    return jsonify({"value": True,
                                    "message": "Logged in",
                                    "token": token})
        return jsonify({"value": False,
                        "message": "Wrong E-Mail or address"})


@api.route('/permission')
class Permission(Resource):
    @token_required
    def get(self):
        return jsonify({"value": True,
                        "message": "Logged in"})


@api.route('/register')
class Register(Resource):
    def post(self):
        email = request.json['address']
        password = request.json['password']
        if email:
            existing_user = User.query.filter_by(address=email).first()
            if existing_user:
                if existing_user.authenticated:
                    return jsonify({"value": False,
                                    "message": "That E-Mail address already exists. Please choose a different one."})
                else:
                    db.session.delete(existing_user)
                    db.session.commit()

            serializer = itsdangerous.URLSafeTimedSerializer(Config.SECRET_KEY)
            token = serializer.dumps(email, salt='user-confirmation')

            hashed_password = bcrypt.generate_password_hash(password)
            new_user = User(address=email, password=hashed_password)  # type: ignore
            db.session.add(new_user)

            db.session.commit()

            confirm_url = url_for('user_confirm_email', _external=True, token=token)
            message_body = f'Please click the following link to confirm your account: ' \
                           f'<a href="{confirm_url}">Click here to confirm address</a>'

            msg = Message('HandReader: Confirm address', sender=Config.MAIL_SENDER_ADDRESS, html=message_body,
                          recipients=[email])
            mail.send(msg)

            return jsonify({"value": True,
                            "message": "Registered"})
        return jsonify({"value": False,
                        "message": "Something went wrong."})


@api.route('/confirm_email')
class ConfirmEmail(Resource):
    def get(self):
        token = request.args.get('token')
        # Verify the token to ensure that it's valid and retrieve the user's email address
        serializer = itsdangerous.URLSafeTimedSerializer(Config.SECRET_KEY)
        try:
            email = serializer.loads(token, salt='user-confirmation', max_age=86400)
        except itsdangerous.SignatureExpired:
            return jsonify({"value": False,
                            "message": "Confirmation link has expired."})
        except itsdangerous.BadSignature:
            return jsonify({"value": False,
                            "message": "Invalid confirmation link."})

        # Mark the user's email as confirmed in the database

        user = User.query.filter_by(address=email).first()
        user.authenticated = True
        db.session.commit()

        return jsonify({"value": True,
                        "message": "Email confirmed!"})


@api.route('/forgot_password')
class ForgotPassword(Resource):
    def post(self):
        email = request.json['address']

        serializer = itsdangerous.URLSafeTimedSerializer(Config.SECRET_KEY)

        existing_reset_address = PasswordReset.query.filter_by(address=email).first()
        if existing_reset_address:
            try:
                serializer.loads(existing_reset_address.token, salt='password-reset', max_age=3600)
                return jsonify({"value": False,
                                "message": "That E-Mail address already has a pending reset request. "
                                           "Please check your mail!"})
            except itsdangerous.SignatureExpired:
                pass    # 'Password reset link has expired. Crating new one.'

        # Generate a secure token for the user
        token = serializer.dumps(email, salt='password-reset')

        # Store the token in a database or other persistent storage
        new_reset = PasswordReset(address=email, token=token)
        db.session.add(new_reset)
        db.session.commit()

        # Send an email to the user with a link to the password reset form
        reset_url = url_for('user_new_password', _external=True, token=token)
        message_body = f'Please reset your password by clicking on this link: <a href="{reset_url}">Reset password</a>'
        msg = Message('HandReader: Reset Password Request', sender=Config.MAIL_SENDER_ADDRESS, html=message_body,
                      recipients=[email])   # TODO: Connect with front
        mail.send(msg)

        return jsonify({"value": True,
                        "message": "Password reset email sent!"})


@api.route('/new_password')
class NewPassword(Resource):
    def post(self):
        token = request.args.get('token')
        new_hashed_password = bcrypt.generate_password_hash(request.json['new_password'])

        serializer = itsdangerous.URLSafeTimedSerializer(Config.SECRET_KEY)
        try:
            email = serializer.loads(token, salt='password-reset', max_age=3600)
        except itsdangerous.SignatureExpired:
            return jsonify({"value": False,
                            "message": "Password reset link has expired."})
        except itsdangerous.BadSignature:
            return jsonify({"value": False,
                            "message": "Invalid reset link."})

        user = User.query.filter_by(address=email).first()
        user.password = new_hashed_password

        db.session.delete(PasswordReset.query.filter_by(token=token).first())

        db.session.commit()

        return jsonify({"value": True,
                        "message": "New password set successfully."})
