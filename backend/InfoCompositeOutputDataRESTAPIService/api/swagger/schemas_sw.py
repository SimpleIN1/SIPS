from flask_restful_swagger_2 import Schema


# Satellite resource schema
class SatelliteSchemaSwagger(Schema):
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64',
        },
        'name': {
            'type': 'string'
        },
        'tag': {
            'type': 'string'
        },
    }


# DateTime resource schema
class TimeSchemaSwagger(Schema):
    type = 'object'
    properties = {
        'time': {
            'type': 'string'
        },
    }


class DateTimeSchemaSwagger(Schema):
    properties = {
        "times": TimeSchemaSwagger.array(),
    }


class DateSchemaSwagger(Schema):
    type = "object"
    properties = {
        "dates": {},
    }


# Fire value resource schema
class FireValueSchemaSwagger(Schema):
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64',
        },
        'temperature': {
            'type': 'float'
        },
        'longitude': {
            'type': 'float'
        },
        'latitude': {
            'type': 'float'
        },
    }


# Composite resource schema
class CompositeItemSchemaSwagger(Schema):
    type = 'object'
    properties = {
        'composite': {
            'type': 'string'
        },
    }


class CompositeSchemaSwagger(Schema):
    properties = {
        "composites": CompositeItemSchemaSwagger.array(),
    }
