import pprint

from marshmallow import Schema, fields, validates, ValidationError, post_load, post_dump

from api import conf
from api.common.generate_link import CompositeGenerateLink
from api.common.point import CuttingPoint
from api.common.compsite_search import CompositeSearch
from api.common.composite_image import CompositeImage, CompositeTask


class CuttingPointSerializer(Schema):
    id = fields.Integer(required=True)
    longitude = fields.Decimal(required=True)
    latitude = fields.Decimal(required=True)

    @post_load
    def post_load_data(self, in_data, many, *args,**kwargs):
        return CuttingPoint(**in_data)


class CompositeImageSerializer(Schema):
    datetime = fields.Integer(required=True)
    satellite = fields.Integer(required=True)
    composite = fields.Integer(required=True)

    @post_load
    def post_load_data(self, in_data, many, *args,**kwargs):
        return CompositeImage(**in_data)


class CompositeTaskSerializer(Schema):
    points = fields.List(fields.Nested(CuttingPointSerializer))
    images = fields.List(fields.Nested(CompositeImageSerializer), required=True)

    @validates("images")
    def validate_images(self, value, **kwargs):
        if not (0 < len(value) < conf.COUNT_FILE_DOWNLOAD):
            raise ValidationError("The number of images are not in the range from 1 to 10")

    @validates("points")
    def validate_points(self, value, **kwargs):
        if not (2 < len(value) < 10):
            raise ValidationError("The number of points scored must be at least 3 and no more than 10")

        item_min = min(value, key=lambda x: x.id)
        item_max = max(value, key=lambda x: x.id)

        if not (item_min.latitude == item_max.latitude and item_min.longitude == item_max.longitude):
            raise ValidationError("The first point and the last point must be equals")

    @post_load
    def post_load_data(self, in_data, many, *args,**kwargs):
        return CompositeTask(**in_data)


class CompositeSearchSerializer(Schema):
    points = fields.List(fields.Nested(CuttingPointSerializer))
    datetimes = fields.List(fields.Integer)
    satellites = fields.List(fields.Integer)
    composites = fields.List(fields.Integer)

    @validates("points")
    def validate_points(self, value, **kwargs):
        if not (2 < len(value) < 10):
            raise ValidationError("The number of points scored must be at least 3 and no more than 10")

        item_min = min(value, key=lambda x: x.id)
        item_max = max(value, key=lambda x: x.id)

        if not (item_min.latitude == item_max.latitude and item_min.longitude == item_max.longitude):
            raise ValidationError("The first point and the last point must be equals")

    @post_load
    def post_load_data(self, in_data, many, *args,**kwargs):
        return CompositeSearch(**in_data)


class CompositeGenerateLinkSerializer(Schema):
    images = fields.List(fields.Nested(CompositeImageSerializer), required=True)

    @post_load
    def post_load_data(self, in_data, many, *args,**kwargs):
        return CompositeGenerateLink(**in_data)

    @validates("images")
    def validate_points(self, value, **kwargs):
        if not (1 <= len(value) < 10):
            raise ValidationError("The number of images scored must be at least 1 and no more than 10")


class DownloadLinkSerializer(Schema):
    id = fields.Integer(required=True)
    link = fields.String(required=True)
    datetime_expiration = fields.String(required=True)


class DownloadHistorySerializer(Schema):
    id = fields.Integer(required=True)
    datetime_download = fields.String(required=True)
    datetime_composite = fields.Integer(required=True)
    satellite = fields.Integer(required=True)
    composite = fields.Integer(required=True)
    is_object_cut = fields.Bool(required=True)


class PaginationSerializer(Schema):
    total = fields.Integer(required=True)
    pages = fields.Integer(required=True)
    page = fields.Integer(required=True)
    has_next = fields.Bool(required=True)
    has_prev = fields.Bool(required=True)
