from datetime import datetime

from api.common.input_params import InputParams
from api.db.models import *


class Composite(InputParams):
    def get_composites(self):
        combined_datetime = datetime.combine(self.date, self.time)
        composites = db.session.execute(
            db.select(
                CompositeModel.name,
            )
            .join(
                FileCompositeModel,
                CompositeModel.id == FileCompositeModel.composite_id
            )
            .join(
                SatelliteModel,
                FileCompositeModel.satellite_id == SatelliteModel.id
            )
            .join(
                DateTimeModel,
                FileCompositeModel.datetime_id == DateTimeModel.id
            )
            .where(
                (SatelliteModel.tag == self.satellite_tag) &
                (DateTimeModel.datetime == combined_datetime) &
                FileCompositeModel.is_downloadable_tiles
            )
            .group_by(CompositeModel.name)
        )

        return composites


class CompositeName:
    def get_by_id(self, id: int):
        return db.get_or_404(CompositeModel, id)

    def get_composites(self):
        composites = db.session.execute(
            db.select(
                CompositeModel.id, CompositeModel.name,
            )
        )

        return composites
