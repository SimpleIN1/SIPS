from datetime import datetime, timedelta

from flask_restful_swagger_2 import Resource, swagger, abort
from webargs import fields, validate
from webargs.flaskparser import use_args

from api.common.caching import cache
from api.db.schemas import CompositeNameSchema
from api.common.composite import Composite, CompositeName
from api.swagger.schemas_sw import CompositeSchemaSwagger, CompositeNameSchemaSwagger
from api.conf import REGEX_PARAMS_SATELLITE


class CompositeResource(Resource):
    @swagger.doc({
        "tags": ["Composite"],
        "summary": "Get Composites",
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
                "name": "time",
                "description": "Time format: HH-MM (example: 07-20)",
                "in": "path",
                "type": "string",
                "required": True
            }
        ],
        "responses": {
            "200": {
                "description": "Returns a composite list by date, satellite, time",
                "schema": CompositeSchemaSwagger,
                "examples": {
                    "application/json": {
                        "composites": [
                            "aot550",
                            "aotaps",
                            "clmsk",
                            "clmsk2",
                            "clphs",
                            "frmsk",
                            "vievi",
                            "vindvi",
                            "vlst",
                            "vscmo"
                        ]
                    }
                }
            }
        }
     })
    @use_args({
        "satellite": fields.String(required=True, validate=validate.Regexp(REGEX_PARAMS_SATELLITE)),
        "date":      fields.Date(format="%Y-%m-%d", required=True),
        "time":      fields.Time(format="%H-%M", required=True),
    }, location="view_args")
    def get(self, *args, **kwargs):
        date = args[0]['date']
        satellite_tag = kwargs['satellite']
        time = args[0]['time']

        key = f"composite_{satellite_tag}_{date}_{time}"
        cached_composites = cache.get(key)

        if not cached_composites:
            composites = Composite(satellite_tag=satellite_tag, date=date, time=time).get_composites()
            composite_list = [item.name for item in composites]

            if not composite_list:
                abort(404, description="Composite names not found!")

            cached_composites = {"composites": composite_list}

            if datetime.utcnow().date() - timedelta(days=15) < date and composite_list:
                cache.set(key, cached_composites, 24 * 60 * 60)

        return cached_composites


class CompositeNameResource(Resource):
    @swagger.doc({
        "tags": ["Composite"],
        "summary": "Get composite",
        "parameters": [
            {
                "name": "id",
                "description": "Composite id",
                "in": "path",
                "type": "integer",
                "required": True
            },
        ],
        "responses": {
            "200": {
                "description": "Returns a satellite by id",
                "schema": CompositeNameSchemaSwagger,
                "examples": {
                    "application/json": {
                        "id": 1,
                        "name": "aot550",
                    }
                }
            }
        }
     })
    def get(self, id):
        cn = CompositeName()
        composite = cn.get_by_id(id)

        serialized = CompositeNameSchema().dump(composite)

        return serialized


class CompositeNameListResource(Resource):
    @swagger.doc({
        "tags": ["Composite"],
        "summary": "Get Composites",
        "responses": {
            "200": {
                "description": "Returns a Composites",
                "schema": CompositeNameSchemaSwagger,
                "examples": {
                    "application/json": [
                        {
                            "id": 1,
                            "name": "aot550",
                        },
                        {
                            "id": 2,
                            "name": "clmsk",
                        }
                    ]
                }
            }
        }
     })
    def get(self):

        cn = CompositeName()
        cached_composites = cache.get("composite_names")
        if not cached_composites:
            composites = cn.get_composites()
            cached_composites = CompositeNameSchema(many=True).dump(composites)
            cache.set("composite_names", cached_composites, 48 * 60 * 60)

        return cached_composites
