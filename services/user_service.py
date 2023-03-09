import itsdangerous
from models.user_model import User
from exts import db, bcrypt, mail
from flask import url_for, jsonify
import jwt
from config import Config
import datetime
from flask_mail import Message
from models.password_reset_model import PasswordReset


def login_user(json_data):
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


def register_user(email, password):
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

def confirm_email(token):
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


def forgot_password(email):
    serializer = itsdangerous.URLSafeTimedSerializer(Config.SECRET_KEY)

    existing_user = User.query.filter_by(address=email).first()
    if not existing_user:
        return jsonify({"value": False,
                        "message": "There is no user with this Address"})

    existing_reset_address = PasswordReset.query.filter_by(address=email).first()
    if existing_reset_address:
        try:
            serializer.loads(existing_reset_address.token, salt='password-reset', max_age=3600)
            return jsonify({"value": False,
                            "message": "That E-Mail address already has a pending reset request. "
                                       "Please check your mail!"})
        except itsdangerous.SignatureExpired:
            # 'Password reset link has expired. Crating new one.'
            db.session.delete(existing_reset_address)
            db.session.commit()

    # Generate a secure token for the user
    token = serializer.dumps(email, salt='password-reset')

    # Store the token in a database or other persistent storage
    new_reset = PasswordReset(address=email, token=token)
    db.session.add(new_reset)
    db.session.commit()

    # Send an email to the user with a link to the password reset form
    reset_url = Config.FRONTEND_URL + 'new_password/' + token
    message_body = f'Please reset your password by clicking on this link: <a href="{reset_url}">Reset password</a>'
    msg = Message('HandReader: Reset Password Request', sender=Config.MAIL_SENDER_ADDRESS, html=message_body,
                  recipients=[email])
    mail.send(msg)

    return jsonify({"value": True,
                    "message": "Password reset email sent!"})


def set_new_password(token, new_password):
    new_hashed_password = bcrypt.generate_password_hash(new_password)
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
