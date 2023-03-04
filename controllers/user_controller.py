from flask_restx import Namespace, Resource
from flask import render_template, make_response, request
from flask_login import login_user, login_required, logout_user
from exts import db, bcrypt
from models.user_model import User


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
