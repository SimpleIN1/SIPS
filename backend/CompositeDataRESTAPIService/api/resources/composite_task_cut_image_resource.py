import pprint
import pickle

from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful_swagger_2 import Resource, swagger, abort

from api import conf
from api.celery.tasks import cut_tiff_images_by_points
from api.common.composite_image import CompositeTask, CompositeTaskContainer, CompositeCutService
from api.common.compsite_search import CompositeSearchService, CompositeSearch
from api.serializers.composite_serializer import CompositeSearchSerializer, \
    CompositeImageSerializer, CompositeTaskSerializer
from api.swagger.schemas_sw import CompositeTaskCutImageSchemaSwagger

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
  "images": [
    {
      "datetime": 18,
      "satellite": 33,
      "composite": 161
    },
    {
      "datetime": 18,
      "satellite": 33,
      "composite": 162
    },
    {
      "datetime": 18,
      "satellite": 33,
      "composite": 163
    }
  ]
}
"""


class CompositeTaskCutTiffImageResource(Resource):
    @swagger.doc({
        "tags": ["CompositeTaskCut"],
        "summary": "Cut tiff-images by points",
        "parameters": [
            {
                "in": "body",
                "name": "body",
                "description": "Requested data.",
                "schema": CompositeTaskCutImageSchemaSwagger,
            },
        ],
        "responses": {
            "200": {
                "description": "Returns images that intersect user polygon",
                "examples": {
                    "application/json": {
                        "message": "Tiff images are sent to cut by points"
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

        serializer = CompositeTaskSerializer()
        ct_data: CompositeTask = None

        try:
            ct_data = serializer.load(request.get_json(), partial=True)
        except ValidationError as e:
            abort(
                400,
                message='Invalid attributes',
                fields=e.messages,
                status=400
            )

        user_id = 1 if conf.TEST_USER else get_jwt().get("user_id")
        email = conf.TEST_USER_EMAIL if conf.TEST_USER else get_jwt().get("email")

        ctc_data = CompositeTaskContainer(
            images=ct_data.images,
            points=ct_data.points,
            user_id=user_id,
            email=email
        )

        check = CompositeCutService().check_length_carved_images(ct_data.images, user_id)
        if not check:
            abort(400, message="The clipping limit has been exceeded")

        byte_stream = pickle.dumps(ctc_data)
        cut_tiff_images_by_points.delay(byte_stream)

        return {"message": "The Tiff images were sent for point cropping"}
