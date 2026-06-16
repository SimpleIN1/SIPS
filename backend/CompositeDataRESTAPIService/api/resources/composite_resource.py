# import datetime
# import operator
# import os.path
#
# from flask import send_from_directory, request
# from flask_jwt_extended import jwt_required, get_jwt
# from flask_restful_swagger_2 import Resource, swagger, abort
# from marshmallow import ValidationError
# from webargs.flaskparser import use_args
# from webargs import fields, validate
#
# from api import conf
# from api.db import models as m
# from api.common.preparing_dowloading_file import CompositeImage, \
#     form_file_download_obj_to_db, CompositePreparing
# # from api.db.requests import FileDownloadDB, FileCompositeDB, UserFileDownloadDB
# from api.serializers.composite_serializer import CompositePreparingSerializer, CompositeImageSerializer
# from api.swagger.schemas_sw import CompositePreparingUrlSchemaSwagger, CompositeSearchSchemaSwagger
#
#
# class CompositePreparingUrlResource(Resource):
#     @swagger.doc({
#         "tags": ["CompositePreparingUrl"],
#         "summary": "Get url to download file",
#         "parameters": [
#             {
#                 "in": "body",
#                 "name": "body",
#                 "description": "Requested data. Datetime format - YYYY-MM-DD HH:MM:SS",
#                 "schema": CompositePreparingUrlSchemaSwagger,
#             },
#         ],
#         "responses": {
#             "200": {
#                 "description": "Returns a url for file downloading and preview",
#                 "examples": {
#                     "application/json": {
#                         "images": [
#                             {
#                                 "datetime": "2023-06-17 07:20:00",
#                                 "satellite": "snpp",
#                                 "composite": "aot550",
#                                 "url": f"http://127.0.0.1:5000/{conf.MAIN_ROUTE}/composites/download/27813c73"
#                             }
#                         ]
#                     }
#                 }
#             }
#         },
#         "security": [
#             {"api_key": []},
#         ],
#      })
#     @jwt_required()
#     def post(self, *args, **kwargs):
#         user_id = get_jwt()["user_id"]
#         serializer = CompositePreparingSerializer()
#         composite_preparing = None
#
#         try:
#             composite_preparing = serializer.load(request.get_json())
#         except ValidationError as e:
#             abort(
#                 400,
#                 message='Invalid attributes',
#                 fields=e.messages,
#                 status=400
#             )
#
#         # file_download_db = FileDownloadDB()
#         # file_composite_db = FileCompositeDB()
#         file_download_db = ()
#         file_composite_db = ()
#
#         # count = file_download_db.get_count_files_to_download_by_user(user_id)
#         # if count > conf.COUNT_FILE_DOWNLOAD:
#         #     abort(
#         #         403,
#         #         message=f"File download limit exceeded ( > {conf.COUNT_FILE_DOWNLOAD})"
#         #     )
#
#         file_composite_items = file_composite_db.get(composite_preparing.images)
#         composite_images = [
#             CompositeImage(
#                 filename=item[0].filename, datetime=item[1].datetime,
#                 satellite=item[2].tag, composite=item[3].name
#             ) for item in file_composite_items
#         ]
#
#         file_download_items = form_file_download_obj_to_db(composite_images, user_id)
#         res = file_download_db.load_urls_downloading(file_download_items)
#         if not res:
#             abort(400, message="Error written")
#
#         return {
#             "images": CompositeImageSerializer(many=True).dump(composite_images)
#         }
#
#
# class CompositeDownloadResource(Resource):
#     @swagger.doc({
#         "tags": ["CompositeDownload"],
#         "summary": "Download Composites Data (download tif image or archive) by uid",
#         "parameters": [
#             {
#                 "name": "uid",
#                 "description": "unique identifier to file for downloading (8 characters)",
#                 "in": "path",
#                 "type": "string",
#                 "required": True
#             },
#         ],
#         "responses": {
#             "200": {
#                 "description": "Returns tiff image or a set of the tiff images into archive",
#                 "examples": {
#                     "image/tiff": {
#                         "schema": {
#                             "type": "string",
#                             "format": "binary"
#                         }
#                     }
#                 }
#             }
#         },
#         "security": [
#             {"api_key": []},
#         ],
#     })
#     @jwt_required()
#     @use_args({
#         "uid": fields.String(required=True, validate=validate.Regexp(conf.REGEX_PARAMS_URL))
#     }, location="view_args")
#     def get(self, *args, **kwargs):
#         uid = kwargs['uid']
#         user_id = get_jwt()["user_id"]
#
#         user_file_download_db = UserFileDownloadDB()
#         file_download_db = FileDownloadDB()
#
#         count = user_file_download_db.get_count_downloaded_files_by_user(user_id)
#         if count > conf.COUNT_FILE_DOWNLOAD - 1:
#             abort(
#                 403, message=f"File download limit exceeded ( > {conf.COUNT_FILE_DOWNLOAD})"
#             )
#
#         instance = file_download_db.get_by_uid(uid)
#         directory = os.path.dirname(instance.filename)
#         filename = os.path.basename(instance.filename)
#
#         user_file_download_db.insert_user_file_download_obj(
#             m.UserFileDownloadModel(
#                 user_id=user_id, file_download_id=instance.uid, datetime_created=datetime.datetime.utcnow()
#             )
#         )
#
#         return send_from_directory(directory, filename, as_attachment=True)
