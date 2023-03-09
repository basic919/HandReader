from flask_restx import Namespace, Resource
from ClassificationModel import ClassificationModel
from flask import request
from models.user_model import token_required
from services.classification_service import predict_number


api = Namespace('classification', description="A namespace for Classification")


model = ClassificationModel()


@api.route('/predict')
class Predict(Resource):
    @token_required
    def post(self):
        return predict_number(model, request.files['image'])


