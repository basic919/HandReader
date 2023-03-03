from flask_restx import Api

from controllers.user_controller import api as user_ns
# from controllers.classification_controller import api as classification_ns

api = Api(
    title='HandReader REST API',
    version='0.1',
    description='This is HandReader API',
    # All API metadata
)

api.add_namespace(user_ns)
#api.add_namespace(classification_ns)
