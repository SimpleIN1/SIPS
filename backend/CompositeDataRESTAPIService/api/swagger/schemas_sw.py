import datetime

from flask_restful_swagger_2 import Schema


# Composite download
class CuttingPointSchemaSwagger(Schema):
    type = "object"
    properties = {
        "id": {
            "type": "integer"
        },
        "longitude": {
            "type": "number"
        },
        "latitude": {
            "type": "number"
        }
    }


class CompositeImageSchemaSwagger(Schema):
    type = "object"
    properties = {
        "datetime": {
            "type": "integer"
        },
        "satellite": {
            "type": "integer"
        },
        "composite": {
            "type": "integer"
        },
    }


class CompositeGenerateUrlSchemaSwagger(Schema):
    properties = {
        "images": CompositeImageSchemaSwagger.array(),
    }


class CompositeSearchImageSchemaSwagger(Schema):
    type = "object"
    properties = {
        "datetime": {
            "type": "string"
        },
        "satellite": {
            "type": "string"
        },
        "composite": {
            "type": "string"
        },
    }


class CompositeDatetimeSearchSchemaSwagger(Schema):
    type = "integer"


class CompositeSatelliteSearchSchemaSwagger(Schema):
    type = "integer"


class CompositeCompositeSearchSchemaSwagger(Schema):
    type = "integer"


class CompositeSearchSchemaSwagger(Schema):
    properties = {
        "points": CuttingPointSchemaSwagger.array(),
        "datetimes": CompositeDatetimeSearchSchemaSwagger.array(),
        "satellites": CompositeSatelliteSearchSchemaSwagger.array(),
        "composites": CompositeCompositeSearchSchemaSwagger.array(),
    }


class CompositeTaskCutImageSchemaSwagger(Schema):
    properties = {
        "points": CuttingPointSchemaSwagger.array(),
        "images": CompositeImageSchemaSwagger.array(),
    }
