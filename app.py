from flask import Flask, render_template, url_for, redirect, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

from exts import db, bcrypt, login_manager
from models.user_model import User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'lkghIUG80yIUOtyIIN07giyOIFG78'

db.init_app(app)
bcrypt.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'login'  # provjeri


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     address = db.Column(db.String(40), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)


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


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/migrate')
def migrate():
    with app.app_context():
        db.create_all()
        print("migrated")
        return "migrated"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(address=form.address.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

# @app.route('/loginx', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(address=form.address.data).first()
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 login_user(user)
#                 return redirect(url_for('dashboard'))
#     return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(address=form.address.data, password=hashed_password)  # type: ignore
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("migrated")

    #app.run(debug=True)
