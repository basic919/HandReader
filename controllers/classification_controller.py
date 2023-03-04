from flask_restx import Namespace, Resource
from ClassificationModel import ClassificationModel
from flask import request


api = Namespace('classification', description="A namespace for Classification")


model = ClassificationModel()


@api.route('/predict')
class Predict(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if json_data:
            return model.predict(json_data.get("image"))

        return -1
