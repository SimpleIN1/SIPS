import json

from flask_mail import Mail
from flask import Flask, jsonify, Blueprint
from flask_jwt_extended import JWTManager
from flask_restful_swagger_2 import Api, get_swagger_blueprint, Resource, swagger, Schema
from flask_migrate import Migrate
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException

from api import conf
from api.db.base import db
from api.common.caching import cache
from api.common.regex_convertor import RegexConverter
from api.resources.composite_download_resource import CompositeDownloadResource, CompositeDownloadLinkResource
from api.resources.composite_gen_link_resource import CompositeGenerateUrlResource
# from api.resources.composite_resource import CompositePreparingUrlResource, CompositeDownloadResource
from api.resources.composite_search_resource import CompositeSearchResource
from api.resources.composite_task_cut_image_resource import CompositeTaskCutTiffImageResource
from api.common.email import init_mail
from api.resources.download_history_resource import CompositeDownloadHistoryResource

# Flask app
app = Flask(__name__, template_folder="templates")
app.url_map.converters['regex'] = RegexConverter
app.config.from_object('api.conf')

if app.config["DEBUG"]:
    migrate = Migrate(app, db)

# Cross Origin Resource Sharing
cors = CORS(app, resources={r'/api/*': {"origins": "*"}})

# JWT
jwt = JWTManager(app)

# Flask restful
api = Api(
    app,
    api_version='v1.0',
    api_spec_url=conf.API_SPEC_URL,
    add_api_spec_resource=True,
    contact={
        "name": "API Support",
        "email": "serbinovichgs@ict.nsc.ru"
    },
    title="Service REST API Composite Output Data",
    description="Service for providing download,cut images and e.t. output data after processing by the "
                "computing complex for operational data processing of the "
                "VIIRS radiometer of Suomi-NPP, NOAA-20 satellites",
    security_definitions={
        "api_key": {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            "description": "Input example: \"Bearer \<Your token\>\"",
        }
    },
    schemes=["https", "http"],
)


with app.app_context():
    swagger_ui_blueprint = get_swaggerui_blueprint(
        conf.SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        conf.API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Swagger UI",
        }
    )

app.register_blueprint(swagger_ui_blueprint)


# Resources
api.add_resource(CompositeSearchResource, f"/{conf.MAIN_ROUTE}/composites/search")

api.add_resource(CompositeTaskCutTiffImageResource, f"/{conf.MAIN_ROUTE}/composites/task/cut-image")

api.add_resource(CompositeGenerateUrlResource, f"/{conf.MAIN_ROUTE}/composites/generate-link")
api.add_resource(CompositeDownloadResource, f"/{conf.MAIN_ROUTE}/composites/download/<uid>", endpoint="download_by_url")
api.add_resource(CompositeDownloadLinkResource, f"/{conf.MAIN_ROUTE}/composites/download/links")
api.add_resource(CompositeDownloadHistoryResource, f"/{conf.MAIN_ROUTE}/composites/download/history")


# Error handler
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
        "status": e.code,
        "error": e.name,
        "message": e.description,
    })
    response.content_type = "application/json"
    return response


# Caching initialization
cache.init_app(app)

# Database initialization
db.init_app(app)


# Run application
if app.config["DEBUG"] and __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
