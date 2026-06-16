
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful_swagger_2 import Resource, swagger, abort

from api import conf
from api.common.download_history import DownloadHistoryService
from api.common.download_link import DownloadLinkService
from api.common.pagination import Pagination
from api.serializers.composite_serializer import DownloadLinkSerializer, DownloadHistorySerializer, PaginationSerializer


class CompositeDownloadHistoryResource(Resource):
    @swagger.doc({
        "tags": ["CompositeDownloadHistory"],
        "summary": "Download history",
        "parameters": [
            {
                "name": "page",
                "description": "number page",
                "in": "query",
                "type": "integer",
                "required": True
            },
            {
                "name": "per_page",
                "description": "count items on page",
                "in": "query",
                "type": "integer",
                "required": True
            },
        ],
        "responses": {
            "200": {
                "description": "Returns download history",
                "examples": {
                    "application/json": {
                        "items": [
                            {
                                "id": 3,
                                "datetime_download": "2026-06-15 10:56:01.161996",
                                "datetime_composite": 18,
                                "satellite": 33,
                                "composite": 162,
                                "is_object_cut": False
                            }
                        ],
                        "pagination": {
                            "total": 3,
                            "pages": 3,
                            "page": 1,
                            "has_next": True,
                            "has_prev": False
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
    def get(self, *args, **kwargs):
        user_id = 1 if conf.TEST_USER else get_jwt().get("user_id")
        page = int(request.args.get("page"))
        per_page = int(request.args.get("per_page"))

        if page < 1:
            abort(400, message="Invalid page")

        if not (0 < per_page <= 100):
            abort(400, message="Invalid per_page")

        pagination = DownloadHistoryService().list(page, per_page, user_id)

        return {
            "items": DownloadHistorySerializer(many=True).dump(pagination.items),
            "pagination": PaginationSerializer().dump(pagination)
        }
