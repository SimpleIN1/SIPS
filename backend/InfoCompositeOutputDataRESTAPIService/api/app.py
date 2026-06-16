import json

from flask_cors import CORS
from flask_migrate import Migrate
from flask import Flask, jsonify, Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful_swagger_2 import Api, get_swagger_blueprint, swagger
from werkzeug.exceptions import HTTPException

import api.conf as conf
from api.db.base import db
from api.common.caching import cache
from api.common.regex_convertor import RegexConverter
from api.resources.composite_resource import CompositeResource, CompositeNameResource, CompositeNameListResource
from api.resources.datetime_resource import DateResource, DateTimeResource
from api.resources.fire_value_resource import FireValueListResource
from api.resources.satellite_resource import SatelliteListResource, SatelliteResource


# Flask app
app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
app.config.from_object('api.conf')

# if app.config["DEBUG"]:
#     migrate = Migrate(app, db)


# Cross Origin Resource Sharing
cors = CORS(app, resources={r'/api/*': {"origins": "*"}})

# Flask restful swagger 3
api = Api(
    app,
    api_spec_url=conf.API_SPEC_URL,
    api_version="v1.0",
    add_api_spec_resource=True,
    contact={
        "name": "API Support",
        "email": "serbinovichgs@ict.nsc.ru",
    },
    title="Документация по API сервиса информации выходных данных композитов",
    description="Сервис предоставления информации о выходных данных "
                "после обработки вычислительным комплексом для оперативной "
                "обработки данных радиометра VIIRS спутников Suomi-NPP, NOAA-20",
    schemes=["http", "https"],
    terms="https://www.google.com/policies/terms/"
)


# Swagger
SWAGGER_URL = f"{conf.API_SPEC_URL}"  # URL for exposing Swagger UI (without trailing '/')
API_URL = f"{conf.API_SPEC_URL}.json"  # Our API url (can of course be a local resource)

with app.app_context():
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Swagger UI",
        }
    )

app.register_blueprint(swagger_ui_blueprint)


# Resources
api.add_resource(DateResource, f"{conf.MAIN_ROUTE}/dates/<satellite>")
api.add_resource(DateTimeResource, f"{conf.MAIN_ROUTE}/dates/times/<satellite>/<date>")

api.add_resource(CompositeNameListResource, f"{conf.MAIN_ROUTE}/composites")
api.add_resource(CompositeNameResource, f"{conf.MAIN_ROUTE}/composites/<int:id>")
api.add_resource(CompositeResource, f"{conf.MAIN_ROUTE}/composites/<satellite>/<date>/<time>")

api.add_resource(FireValueListResource, f"{conf.MAIN_ROUTE}/fire-values/<satellite>/<date>/<resolution>")

api.add_resource(SatelliteListResource, f"{conf.MAIN_ROUTE}/satellites")
api.add_resource(SatelliteResource, f"{conf.MAIN_ROUTE}/satellites/<int:id>")


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

# with app.app_context():
#     import api.db.models
    # db.create_all()
    # db.drop_all()


# Run application
if app.config["DEBUG"] and __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
