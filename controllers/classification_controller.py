from flask_restx import Namespace, Resource, fields
from flask import Blueprint
from ClassificationModel import ClassificationModel
from flask import render_template, redirect, url_for, make_response


#api = Namespace('classification', description="A namespace for Classification")


my_bp = Blueprint('my_bp', __name__, url_prefix='/classification')


model = ClassificationModel()


@my_bp.route('/predict', methods=['GET'])   # TODO: Change this to POST
# @api.route('/predict')
def get():
    print('predicting...')
    return model.predict()
