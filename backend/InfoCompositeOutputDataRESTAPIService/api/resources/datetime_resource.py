from flask_restful_swagger_2 import Resource, swagger, abort
from webargs import fields
from webargs.flaskparser import use_args

from api.common.date_time import DateService, DateTime
from api.swagger.schemas_sw import DateTimeSchemaSwagger, DateSchemaSwagger
from api.common.caching import cache


class DateResource(Resource):
    @swagger.doc({
        "tags": ["DateTime"],
        "summary": "Get Dates",
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
    def get(self):
        date_s = DateService()
        cached_dates = cache.get("dates")

        if not cached_dates:
            items = date_s.get_dates()
            cached_dates = date_s.format_dates(items)
            if cached_dates:
                cache.set("dates", cached_dates, 6 * 60 * 60)

        return cached_dates


class DateTimeResource(Resource):
    @swagger.doc({
        "tags": ["DateTime"],
        "summary": "Get Times",
        "parameters": [
            {
                "name": "date",
                "description": "Date format: YYYY-MM-DD (example: 2023-06-17)",
                "in": "path",
                "type": "string",
                "required": True
            }
        ],
        "responses": {
            "200": {
                "description": "Returns a time by date",
                "schema": DateTimeSchemaSwagger,
                "examples": {
                    "application/json": {
                        "times": [
                            "07:20"
                        ]
                    }
                }
            }
        }
     })
    @use_args({
        "date": fields.Date(format="%Y-%m-%d", required=True),
    }, location="view_args")
    def get(self, *args, **kwargs):
        date = kwargs.get("date")

        date_time = DateTime(date=date)
        datetime_items = date_time.get_datetimes()
        formatted_times = date_time.fetch_times(datetime_items)

        if not formatted_times:
            abort(404, description="Times not found!")

        return {"times": formatted_times}
