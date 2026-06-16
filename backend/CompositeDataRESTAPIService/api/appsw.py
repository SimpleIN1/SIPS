from flask import Flask, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
# Instead of using this: from flask_restful import Api
# Use this:
from flask_restful_swagger_2 import Api, Resource, swagger, get_swagger_blueprint
from flask_restful_swagger_2 import Schema
from flask_swagger_ui import get_swaggerui_blueprint
from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config['PROPAGATE_EXCEPTIONS'] = True

# app.config["DEBUG"] = False  # Change this!
jwt = JWTManager(app)


# Use the swagger Api class as you would use the flask restful class.
# It supports several (optional) parameters, these are the defaults:
api = Api(app, api_version='v0.0', add_api_spec_resource=True,
        contact={
            "name": "API Support",
            "email": "serbinovichgs@ict.nsc.ru"
        },
        **{
            'title': 'asdasd',
            'description': 'adasd',
        },
        # security="Bearer Auth",
        security_definitions={
            # 'Bearer Auth': {
            #     'type': 'apiKey',
            #     'in': 'header',
            #     'name': 'Authorization',
            #     "description": "description",
            # },

            "api_key": {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                "description": "Input example: \"Bearer \<Your token\>\"",
            }
        },
        schemes=["http", "https"],
        # authorizations={
        #     'apikey': {
        #         'type': 'apiKey',
        #         'in': 'header',
        #         'name': 'Authorization',
        #         'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
        #     }
        # }
)

cors = CORS(app, resources={r'/api/*': {"origins": "*"}})


def auth(*args, **kwargs):
    # Space for your fancy authentication. Return True if access is granted, otherwise False
    # api_key is extracted from the url parameters (?api_key=foo)
    # endpoint is the full swagger url (e.g. /some/{value}/endpoint)
    # method is the HTTP method
    print(args)
    print(kwargs)
    print("api_key, endpoint, method")
    return True


# swagger.auth = auth

# auth1 = HTTPTokenAuth(scheme='Bearer')
#
# auth1.

def callback(*args, **kwargs):
    return True




# request_schema = {
#     'type': 'object',
#     'properties': {
#         'list': {
#             'type': 'array',
#             'items': {'type': 'string'},
#             'minItems': 1,
#         },
#     },
#     'additionalProperties': False,
#     'required': ['list'],
# }
# request_model = api.schema_model('test_list_request', request_schema)


class MyView(Resource):
    @swagger.doc({
        'tags': ['user1'],
        "security": [
            {"api_key": []},
        ],
        'responses': {
            '201': {
                'description': 'Created group',
                'examples': {
                    'application/json': {
                        'id': 1
                    }
                }
            }
        },
    })
    # @swagger.auth('asdasd', "/api/some/endpoint", "http")
    @jwt_required()
    def get(self, *args, **kwargs):
        print(args)
        current_user = get_jwt_identity()
        # jwt.
        print(kwargs)
        print(current_user)
        return {"1": 1}

    @swagger.doc({
        'tags': ['user2'],
        # "security": [
        #     {"api_key": []},
        # ],
        'responses': {
            '201': {
                'description': 'Created group',
                'examples': {
                    'application/json': {
                        'id': 1
                    }
                }
            }
        },
    })
    def post(self):
        return {}


api.add_resource(MyView, '/api/some/endpoint')


class EmailModel(Schema):
    type = 'string'
    format = 'email'


class KeysModel(Schema):
    type = 'object'
    properties = {
        'name': {
            'type': 'string'
        }
    }


class UserModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64',
        },
        'name': {
            'type': 'string'
        },
        'mail': EmailModel,
        'keys': KeysModel.array()
    }
    required = ['name']


class UserItemResource(Resource):
    @swagger.doc({
        'tags': ['user'],
        # 'description': 'Returns a user',
        'parameters': [
            {
                'name': 'user_id',
                'description': 'User identiываываfier',
                'in': 'path',
                'type': 'integer',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'User',
                'schema': UserModel,
                'examples': {
                    'application/json': {
                        'id': 1,
                        'name': 'somebody'
                    }
                }
            }
        }
     })
    # @jwt_required()
    @use_args({
        "user_id":  fields.Integer(required=True),
    }, location='view_args')
    def get(self, *args, **kwargs):
        # Do some processing
        # current_user = get_jwt_identity()
        print(args)
        print(kwargs)
        return UserModel(id=1, name='somebody'), 200  # generates json response {"id": 1, "name": "somebody"}


@app.route('/')
def index():
    return """<head>
    <meta http-equiv="refresh" content="0; url=http://petstore.swagger.io/?url=http://localhost:5000/api/swagger.json" />
    </head>"""


api.add_resource(UserItemResource, '/api/users/<user_id>')

# def get_user_resources():
#     """
#     Returns user resources.
#     :param app: The Flask instance
#     :return: User resources
#     """
#     blueprint = Blueprint('user', __name__)
#
#     api = Api(blueprint, add_api_spec_resource=False)
#
#     # api.add_resource(UserResource, '/api/users')
#     api.add_resource(UserItemResource, '/api/users/<int:user_id>')
#
#     return api
#
#
# docs = []
#
# # Get user resources
# user_resources = get_user_resources()
#
# # Retrieve and save the swagger document object (do this for each set of resources).
# docs.append(user_resources.get_swagger_doc())
#
# # Register the blueprint for user resources
# app.register_blueprint(user_resources.blueprint)
#
# app.register_blueprint(get_swagger_blueprint(docs, '/api/swagger1', title='Example', api_version='1'))


print(app.url_map)
# print(api.get_swagger_doc())


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://127.0.0.1:5001/api/swagger.json'  # Our API url (can of course be a local resource)


# Call factory function to create our blueprint
with app.app_context():
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application",
            # "title": "Service REST API Composite Output Data",
            # "description": "Service for providing download,cut images and e.t. output data after processing by the",
            # "version":"v1.0",
            # "servers": [],
            # "contact": {
            #     "name": "API Support",
            #     "email": "serbinovichgs@ict.nsc.ru"
            # }
        },
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )

app.register_blueprint(swaggerui_blueprint)



# with app.app_context():
#     swagger_blueprint = get_swagger_blueprint([api.get_swagger_doc()], '/api/swagger2   ', title='Example', api_version='1')
# app.register_blueprint(swagger_blueprint, url_prefix=f"/api/swagger1")
