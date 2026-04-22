from flask_restful_swagger_2 import swagger, Resource

from api.common.satellite import get_satellites, get_satellite_by_id
from api.db.schemas import SatelliteSchema
from api.swagger.schemas_sw import SatelliteSchemaSwagger
from api.common.caching import cache


class SatelliteResource(Resource):
    @swagger.doc({
        "tags": ["Satellite"],
        "summary": "Get Satellite",
        "parameters": [
            {
                "name": "id",
                "description": "Satellite id",
                "in": "path",
                "type": "integer",
                "required": True
            },
        ],
        "responses": {
            "200": {
                "description": "Returns a satellite by id",
                "schema": SatelliteSchemaSwagger,
                "examples": {
                    "application/json": {
                        "id": 1,
                        "name": "Soumi NPP",
                        "tag": "snpp"
                    }
                }
            }
        }
     })
    def get(self, id):
        satellite = get_satellite_by_id(id)
        serialized = SatelliteSchema().dump(satellite)

        return serialized


class SatelliteListResource(Resource):
    @swagger.doc({
        "tags": ["Satellite"],
        "summary": "Get Satellites",
        "responses": {
            "200": {
                "description": "Returns a satellites",
                "schema": SatelliteSchemaSwagger,
                "examples": {
                    "application/json": [
                        {
                            "id": 1,
                            "name": "Soumi NPP",
                            "tag": "snpp"
                        },
                        {
                            "id": 2,
                            "name": "NOAA-20",
                            "tag": "noaa20"
                        }
                    ]
                }
            }
        }
     })
    def get(self):
        cached_satellites = cache.get("satellites")
        if not cached_satellites:
            satellites = get_satellites()
            cached_satellites = SatelliteSchema(many=True).dump(satellites)
            cache.set("satellites", cached_satellites, 48 * 60 * 60)

        return cached_satellites
