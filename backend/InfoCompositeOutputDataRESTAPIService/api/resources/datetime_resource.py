from flask_restful_swagger_2 import Resource, swagger, abort
from flask import request
from webargs import fields, validate
from webargs.flaskparser import use_args

from api.common.caching import cache
from api.conf import REGEX_PARAMS_SATELLITE
from api.common.date_time import DateService, DateTime, DateTimeIdService
from api.swagger.schemas_sw import DateTimeSchemaSwagger, DateSchemaSwagger


class DateResource(Resource):
    @swagger.doc({
        "tags": ["DateTime"],
        "summary": "Get Dates",
        "parameters": [
            {
                "name": "satellite",
                "description": "Satellite example: snpp or noaa20",
                "in": "path",
                "type": "string",
                "required": True
            },
        ],
        "responses": {
            "200": {
                "description": "Returns a dates",
                "schema": DateSchemaSwagger,
                "examples": {
                    "application/json": {
                        "dates": {
                            "2023": {
                                "06": [
                                    "2023-06-27",
                                    "2023-06-26",
                                    "2023-06-23"
                                ]
                            }
                        }
                    }
                }
            }
        }
     })
    @use_args({
        "satellite": fields.String(required=True, validate=validate.Regexp(REGEX_PARAMS_SATELLITE)),
    }, location="view_args")
    def get(self, *args, **kwargs):
        satellite = kwargs['satellite']
        date_s = DateService()
        cached_dates = cache.get(f"dates_{satellite}")

        if not cached_dates:
            items = date_s.get_dates(satellite)
            cached_dates = date_s.format_dates(items)
            if cached_dates:
                cache.set(f"dates_{satellite}", cached_dates, 6 * 60 * 60)

        return cached_dates


class DateTimeResource(Resource):
    @swagger.doc({
        "tags": ["DateTime"],
        "summary": "Get Times",
        "parameters": [
            {
                "name": "satellite",
                "description": "Satellite example: snpp or noaa20",
                "in": "path",
                "type": "string",
                "required": True
            },
            {
                "name": "date",
                "description": "Date format: YYYY-MM-DD (example: 2023-06-17)",
                "in": "path",
                "type": "string",
                "required": True
            },
        ],
        "responses": {
            "200": {
                "description": "Returns a time by date",
                "schema": DateTimeSchemaSwagger,
                "examples": {
                    "application/json": {
                        "times": [
                            {
                                "time": "07:20",
                                "datetime": "2023-06-17 07:20",
                                "id": 14
                            }
                        ]
                    }
                }
            }
        }
    })
    @use_args({
        "satellite": fields.String(required=True, validate=validate.Regexp(REGEX_PARAMS_SATELLITE)),
        "date": fields.Date(format="%Y-%m-%d", required=True),
    }, location="view_args")
    def get(self, *args, **kwargs):
        date = kwargs.get("date")
        satellite = kwargs.get("satellite")

        date_time = DateTime(date=date, satellite_tag=satellite)
        datetime_items = date_time.get_datetimes()
        formatted_times = date_time.fetch_times(datetime_items)

        if not formatted_times:
            abort(404, description="Times not found!")

        return {"times": formatted_times}


"""
"""


class DateTimeIdResource(Resource):
    @swagger.doc({
        "tags": ["DateTime"],
        "summary": "Get Times",
        "parameters": [
            {
                "name": "datetime_start_id",
                "description": "Param format: integer (example: 20)",
                "in": "query",
                "type": "string",
                "required": False
            },
            {
                "name": "datetime_stop_id",
                "description": "Param format: integer (example: 20)",
                "in": "query",
                "type": "string",
                "required": False
            },
        ],
        "responses": {
            "200": {
                "description": "Returns a time and id",
                "examples": {
                    "application/json": {
                        "times": {
                            "20": "2023-06-17 07:20",
                            "21": "2023-06-18 07:01"
                        }
                    }
                }
            }
        }
    })
    @use_args({
        "datetime_start_id": fields.Integer(required=False),
        "datetime_stop_id":  fields.Integer(required=False),
    }, location="query")
    def get(self, *args, **kwargs):
        datetime_start_id = args[0].get("datetime_start_id")
        datetime_stop_id = args[0].get("datetime_stop_id")

        if datetime_start_id and datetime_stop_id and not (datetime_stop_id >= datetime_start_id):
            abort(400, message="datetime_stop_id must be greater than datetime_start_id")

        dti_service = DateTimeIdService()
        items = dti_service.get_datetimes(datetime_start_id, datetime_stop_id)

        if not items:
            abort(404, message="Times not found")

        format_items = dti_service.format(items)

        return {"times": format_items}
