from datetime import datetime

from sqlalchemy import func

from api.common.input_params import InputParams
from api.db.models import *


class FireValue(InputParams):
    def __init__(self, resolution, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resolution = resolution

    def get_fire_values(self):
        if self.time:
            combined_datetime = datetime.combine(self.date, self.time)
            datetime_expression = (DateTimeModel.datetime == combined_datetime)
        else:
            datetime_expression = (func.to_char(DateTimeModel.datetime, "YYYY-MM-DD") == str(self.date))

        fire_values = db.session.execute(
            db.select(
                FireValueModel.temperature,
                FireValueModel.longitude,
                FireValueModel.latitude,
                DateTimeModel.datetime,
                SatelliteModel.tag.label('satellite')
            )
            .join(
                SatelliteModel,
                FireValueModel.satellite_id == SatelliteModel.id
            )
            .join(
                DateTimeModel,
                FireValueModel.datetime_id == DateTimeModel.id
            )
            .where(
                (SatelliteModel.tag == self.satellite_tag) & datetime_expression &
                (FireValueModel.resolution == FireValueModel.RESOLUTION_SATELLITE[self.resolution])
            )
        ).all()
        return fire_values
