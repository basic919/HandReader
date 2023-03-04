from flask_restx import Namespace, Resource
from ClassificationModel import ClassificationModel
from flask import request


api = Namespace('classification', description="A namespace for Classification")


model = ClassificationModel()


@api.route('/predict')
class Predict(Resource):    # TODO: Change this to POST
    def get(self):
        return model.predict()
