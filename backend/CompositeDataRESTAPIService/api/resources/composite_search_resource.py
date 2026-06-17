import pprint

from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful_swagger_2 import Resource, swagger, abort

from api.common.compsite_search import CompositeSearchService, CompositeSearch
from api.serializers.composite_serializer import CompositeSearchSerializer, \
    CompositeImageSerializer
from api.swagger.schemas_sw import CompositeSearchSchemaSwagger


"""

{
  "points": [
    {
      "id": 1,
      "longitude": 49.15,
      "latitude": 55.74
    },
    {
      "id": 2,
      "longitude": 60.71,
      "latitude": 50.83
    },
    {
      "id": 3,
      "longitude": 57.24,
      "latitude": 50.24
    },
    {
      "id": 4,
      "longitude": 49.15,
      "latitude": 55.74
    }
  ],
  "datetimes": [
    18
  ],
  "satellites": [
    33
  ],
  "composites": [
    161
  ]
}

"""


class CompositeSearchResource(Resource):
    @swagger.doc({
        "tags": ["CompositeSearch"],
        "summary": "Search the composites by points",
        "parameters": [
            {
                "in": "body",
                "name": "body",
                "description": "Requested data.",
                "schema": CompositeSearchSchemaSwagger,
            },
        ],
        "responses": {
            "200": {
                "description": "Returns images that intersect user polygon",
                "examples": {
                    "application/json": {
                        "images": [
                            {
                                "datetime": 14,
                                "satellite": 23,
                                "composite": 112,
                            }
                        ]
                    }
                }
            }
        },
        "security": [
            {"api_key": []},
        ],
    })
    @jwt_required()
    def post(self, *args, **kwargs):
        serializer = CompositeSearchSerializer()
        cs_data: CompositeSearch = None

        try:
            cs_data = serializer.load(request.get_json(), partial=True)
        except ValidationError as e:
            abort(
                400,
                message='Invalid attributes',
                fields=e.messages,
                status=400
            )

        cs = CompositeSearchService()
        images = cs.search(cs_data.points, cs_data.datetimes, cs_data.satellites, cs_data.composites)

        if not images:
            abort(404, message="Images not found")

        return {"images": CompositeImageSerializer(many=True).dump(images)}
