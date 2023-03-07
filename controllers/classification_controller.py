from flask_restx import Namespace, Resource
from ClassificationModel import ClassificationModel
from flask import request
from models.user_model import token_required


api = Namespace('classification', description="A namespace for Classification")


model = ClassificationModel()


@api.route('/predict')
class Predict(Resource):
    @token_required
    def post(self):
        image = request.files['image']
        if image:
            return model.predict(image)
        return -1
