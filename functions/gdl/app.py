from flask import Flask, jsonify, Blueprint
from flask_restplus import Api, Resource, Namespace

import game_controller
import language_controller
from models import ValidationError

blueprint = Blueprint('api', __name__)

authorizations = {
    'oauth2': {
        'type': 'oauth2',
        'flow': 'implicit',
        'authorizationUrl': 'https://digitallibrary.eu.auth0.com/authorize',
        'scopes': {
            'games:all': 'Grant full access to games',
        }
    }
}


api = Api(blueprint, description="Api for retrieving games from the GDL", authorizations=authorizations, version='1.0',
          terms_url='https://digitallibrary.io', contact='Christer Gundersen',
          contact_email='christer@digitallibrary.io', contact_url='https://digitallibrary.io',
          license='Apache License 2.0', license_url='https://www.apache.org/licenses/LICENSE-2.0', doc=False)

api.add_namespace(language_controller.API, path='/languages')
api.add_namespace(game_controller.API, path='/games')

DOC_API = Namespace('api-docs', description="API Documentation for the API")


@DOC_API.route("/", strict_slashes=False)
@DOC_API.doc(False)
class ApiDocumentation(Resource):
    def get(self):
        swagger = api.__schema__
        swagger['basePath'] = '/game-service/v1'
        return jsonify(api.__schema__)


docprint = Blueprint('doc', __name__)
docApi = Api(docprint, description="Documentation for APIs")
docApi.add_namespace(DOC_API, path='/')

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/'
app.register_blueprint(blueprint, url_prefix='/game-service/v1', doc='/doc/')
app.register_blueprint(docprint, url_prefix='/game-service/api-docs')


@api.errorhandler(ValidationError)
@app.errorhandler(ValidationError)
def handle_validation_error(error):
    """When a validation error occurs"""
    return error.json(), 400


if __name__ == "__main__":
    app.run()
