from flask_restx import Namespace, Resource, fields
from ClassificationModel import ClassificationModel
from flask import render_template, redirect, url_for, make_response


api = Namespace('classification', description="A namespace for Classification")


model = ClassificationModel()


# TODO: Change this to POST
@api.route('/predict')
class Predict(Resource):
    def get(self):
        return model.predict()
