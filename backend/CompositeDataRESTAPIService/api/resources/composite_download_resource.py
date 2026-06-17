import os

from flask_mail import Message
from webargs import fields, validate
from marshmallow import ValidationError
from webargs.flaskparser import use_args
from flask import send_from_directory, request
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful_swagger_2 import Resource, swagger, abort

from api import conf
from api.common.download import DownloadService
from api.common.download_history import DownloadHistoryCreated, DownloadHistoryService
from api.common.download_link import DownloadLinkService
from api.serializers.composite_serializer import DownloadLinkSerializer


class CompositeDownloadResource(Resource):
    @swagger.doc({
        "tags": ["CompositeDownload"],
        "summary": "Download Composites Data (download tif image) by uid",
        "parameters": [
            {
                "name": "uid",
                "description": "unique identifier to file for downloading (8 characters)",
                "in": "path",
                "type": "string",
                "required": True
            },
        ],
        'produces': [
            'image/tiff',
        ],
        "responses": {
            "200": {
                "description": "Returns tiff image", #or a set of the tiff images into archive
                'schema': {
                    'type': 'file',
                    "format": "binary"
                },
                "examples": {
                    "image/tiff": {
                        "schema": {
                            "type": "file",
                            "format": "binary"
                        }
                    }
                }
            }
        },
        "security": [
            {"api_key": []},
        ],
    })
    @jwt_required()
    @use_args({
        "uid": fields.String(required=True, validate=validate.Regexp(conf.REGEX_PARAMS_URL))
    }, location="view_args")
    def get(self, *args, **kwargs):
        uid = kwargs['uid']
        user_id = 1 if conf.TEST_USER else get_jwt().get("user_id")

        d_service = DownloadService()
        ## валидация
        if not d_service.check_download_file_length(user_id):
            abort(400, message="The daily file download limit has been exceeded")

        download_item = d_service.get_filename(uid, user_id)
        if not download_item:
            abort(404, message="File not found")

        dh_item = DownloadHistoryCreated(user_id=user_id, download_link_id=download_item.download_link_id)
        DownloadHistoryService().create(dh_item)

        path = os.path.abspath(download_item.filename)
        directory = os.path.dirname(path)
        filename = os.path.basename(path)

        return send_from_directory(directory, filename, as_attachment=True)


class CompositeDownloadLinkResource(Resource):
    @swagger.doc({
        "tags": ["CompositeDownload"],
        "summary": "Download links to download tif image by uid",
        "responses": {
            "200": {
                "description": "Returns download links",
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
    def get(self, *args, **kwargs):
        user_id = 1 if conf.TEST_USER else get_jwt().get("user_id")
        dl_service = DownloadLinkService()
        links = dl_service.get_links(user_id)

        if not links:
            abort(404, message="Links not found")

        return {"links": DownloadLinkSerializer(many=True).dump(links)}
