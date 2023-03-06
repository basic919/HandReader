from flask_restx import Namespace, Resource
from ClassificationModel import ClassificationModel
from flask import request


api = Namespace('classification', description="A namespace for Classification")


model = ClassificationModel()


@api.route('/predict')
class Predict(Resource):
    def post(self):
        image = request.files['image']
        if image:
            return model.predict(image)
        return -1
