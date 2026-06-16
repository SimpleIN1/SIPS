import os

from flask_mail import Message
from webargs import fields, validate
from marshmallow import ValidationError
from webargs.flaskparser import use_args
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful_swagger_2 import Resource, swagger, abort

from api import conf
from api.common.generate_link import CompositeGenerateLinkContainer, GenerateLinkService
from api.serializers.composite_serializer import CompositeGenerateLinkSerializer, DownloadLinkSerializer
from api.swagger.schemas_sw import CompositeGenerateUrlSchemaSwagger


class CompositeGenerateUrlResource(Resource):
    @swagger.doc({
        "tags": ["CompositeGenerateUrl"],
        "summary": "Generate url to download file",
        "parameters": [
            {
                "in": "body",
                "name": "body",
                "description": "Requested data.",
                "schema": CompositeGenerateUrlSchemaSwagger,
            },
        ],
        "responses": {
            "200": {
                "description": "Returns a url for file downloading",
                "examples": {
                    "application/json": {
                        "links": [
                            {
                                "id": 11,
                                "link": "http://127.0.0.1/api/vcd/composites/download/jr3tcyuge9",
                                "datetime_expiration": "2026-07-01 18:34:56.935986"
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
        user_id = 1 if conf.TEST_USER else get_jwt().get("user_id")
        serializer = CompositeGenerateLinkSerializer()
        composite_preparing = None

        try:
            composite_preparing = serializer.load(request.get_json())
        except ValidationError as e:
            abort(
                400,
                message='Invalid attributes',
                fields=e.messages,
                status=400
            )

        # валидация
        gl_service = GenerateLinkService()
        if not gl_service.check_generated_links_length(user_id):
            abort(400, message="The link generation limit has been exceeded")

        cglc_item = CompositeGenerateLinkContainer(user_id=user_id,
                                                   images=composite_preparing.images)

        links = gl_service.create_links(cglc_item)

        return {"links": DownloadLinkSerializer(many=True).dump(links)}
