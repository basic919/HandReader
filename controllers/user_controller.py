from flask_restx import Namespace, Resource
from flask import render_template, redirect, url_for, make_response

from flask_login import login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from exts import db, bcrypt
from models.user_model import User


api = Namespace('user', description="A namespace for User")


# data_sources_model = api.model(
#     "Users",
#     {
#         "id": fields.Integer(),
#         "address": fields.String(),
#         "password": fields.String(),
#     }
# )


@api.route('/home')
class HomeController(Resource):
    def get(self):
        return make_response(render_template('home.html'))


@api.route('/login')
class Login(Resource):
    def get(self):
        form = LoginForm()
        return make_response(render_template('login.html', form=form))

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(address=form.address.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('user_dashboard'))


@api.route('/dashboard')
class Dashboard(Resource):
    @login_required
    def get(self):
        return make_response(render_template('dashboard.html'))


@api.route('/logout')
class Logout(Resource):
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('user_dashboard'))


@api.route('/register')
class Register(Resource):
    def get(self):
        form = RegisterForm()
        return make_response(render_template('register.html', form=form))

    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(address=form.address.data, password=hashed_password)  # type: ignore
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('user_dashboard'))


class RegisterForm(FlaskForm):
    address = StringField(validators=[
                           InputRequired(), Length(min=5, max=40)], render_kw={"placeholder": "E-mail"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_address(self, address):
        existing_user_address = User.query.filter_by(
            address=address.data).first()
        if existing_user_address:
            raise ValidationError(
                'That E-Mail address already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    address = StringField(validators=[
                           InputRequired(), Length(min=5, max=40)], render_kw={"placeholder": "E-Mail"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')
