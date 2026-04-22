from datetime import timedelta, date as d, datetime

from flask_restful_swagger_2 import swagger, Resource, abort
from webargs import fields, validate
from marshmallow import validate as m_validate
from webargs.flaskparser import use_args

from api.common.fire_value import FireValue
from api.common.caching import cache
from api.db.schemas import FireValueSchema
from api.swagger.schemas_sw import FireValueSchemaSwagger
from api.conf import REGEX_PARAMS_SATELLITE


class FireValueListResource(Resource):
    @swagger.doc({
        "tags": ["FireValue"],
        "summary": "Get Fire values",
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
            {
                "name": "resolution",
                "description": "Resolution of data fixation by the satellite spectrometer. "
                               "Resolution example: 375m or 750m",
                "in": "path",
                "type": "string",
                "required": True
            },
            {
                "name": "time",
                "description": "Time format: HH-MM (example: 07-20)",
                "in": "query",
                "type": "string",
                "required": False
            }
        ],
        "responses": {
            "200": {
                "description": "Returns a fire value by date, satellite",
                "schema": FireValueSchemaSwagger,
                "examples": {
                    "application/json": [
                        {
                            "temperature": "337.00",
                            "longitude": "74.16107",
                            "latitude": "32.90946",
                            "satellite": "snpp",
                            "datetime": "2023-06-17T07:20:00"
                        },
                        {
                            "temperature": "367.00",
                            "longitude": "80.83962",
                            "latitude": "36.96287",
                            "satellite": "snpp",
                            "datetime": "2023-06-17T07:20:00"
                        }
                    ]
                }
            }
        }
     })
    @use_args({
        "time":       fields.Time(format="%H-%M", required=False),
    }, location="query")
    @use_args({
        "satellite":  fields.String(required=True, validate=validate.Regexp(REGEX_PARAMS_SATELLITE)),
        "date":       fields.Date(format="%Y-%m-%d", required=True),
        "resolution": fields.String(validate=validate.OneOf(["375m", "750m"]), required=True)
    }, location="view_args")
    def get(self, *args, **kwargs):
        date = args[1]['date']
        satellite_tag = kwargs['satellite']
        time = args[0].get('time')
        resolution = kwargs['resolution']

        tmp_key = f"fire_value_{satellite_tag}_{date}_{resolution}"
        key = tmp_key if not time else tmp_key + f"_{time}"

        cached_fire_value = cache.get(key)

        if not cached_fire_value:
            fire_values = FireValue(
                satellite_tag=satellite_tag, date=date, time=time, resolution=resolution
            ).get_fire_values()

            if not fire_values:
                abort(404, description="Fire values not found!")

            cached_fire_value = FireValueSchema(many=True).dump(fire_values)

            if datetime.utcnow().date() - timedelta(days=10) < date and cached_fire_value:
                cache.set(key, cached_fire_value, 24 * 60 * 60)

        return cached_fire_value
