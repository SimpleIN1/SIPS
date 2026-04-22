from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow import fields

from api.db.models import SatelliteModel, DateTimeModel, FireValueModel


class SatelliteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SatelliteModel
        include_relationship = True
        load_instance = True


class FireValueSchema(SQLAlchemySchema):
    temperature = fields.Decimal(as_string=True)
    longitude = fields.Decimal(as_string=True)
    latitude = fields.Decimal(as_string=True)
    satellite = fields.String()
    datetime = fields.DateTime()

    class Meta:
        # model = FireValueModel
        include_relationship = True
        load_instance = True
