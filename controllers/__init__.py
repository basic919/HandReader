from flask_restx import Api

from controllers.user_controller import api as user_ns

api = Api(
    title='My Title',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(user_ns)