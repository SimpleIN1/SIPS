from sqlalchemy import func

from api.common.input_params import InputParams
from api.db.base import db
from api.db.models import DateTimeModel, CompositeModel, FileCompositeModel, SatelliteModel


class DateService:
    def get_dates(self, satellite: str):
        items = db.session.execute(
            db.select(func.to_char(DateTimeModel.datetime, "YYYY-MM-DD").label("date"))
            .select_from(FileCompositeModel)
            .join(DateTimeModel, DateTimeModel.id == FileCompositeModel.datetime_id)
            .join(SatelliteModel, SatelliteModel.id == FileCompositeModel.satellite_id)
            .where(SatelliteModel.tag == satellite)
            .group_by(func.to_char(DateTimeModel.datetime, "YYYY-MM-DD").label("date"))
        )
        return items

    def format_dates(self, items) -> dict:
        """
        Processing the date received from the database to the format below.
        :params items: the name of the items stores a list of snapshot capture dates
        :return dict: return dict that stores formatted dates by template

        {
            "dates": {
                '2023': {
                    '06': [
                        '2023-06-17',
                        '2023-06-18'
                    ],
                    '07': [
                        '2023-07-11'
                    ]
                },
                '2024': {
                    '04': [
                        '2024-04-28'
                    ]
                }
            }
        }
        """

        tmp_dict = {}

        for item in items:
            # tmp = str(item.datetime.date())
            tmp = str(item.date)
            year, month, day = tmp.split('-')
            tmp_dict.setdefault(year, {})
            tmp_dict[year].setdefault(month, [])
            tmp_dict[year][month].append(tmp)

        return {"dates": tmp_dict}


class DateTime(InputParams):
    def get_datetimes(self):
        datetimes = db.session.execute(
            db.select(DateTimeModel.id, DateTimeModel.datetime)
            .select_from(FileCompositeModel)
            .join(DateTimeModel, DateTimeModel.id == FileCompositeModel.datetime_id)
            .join(SatelliteModel, SatelliteModel.id == FileCompositeModel.satellite_id)
            .where((SatelliteModel.tag == self.satellite_tag)
                   &
                   (func.to_char(DateTimeModel.datetime, "YYYY-MM-DD") == self.date))
            .group_by(DateTimeModel.id, DateTimeModel.datetime)
        )
        return datetimes

    def fetch_times(self, items):
        return [
            {
                "time": item.datetime.strftime("%H:%M"),
                "datetime": item.datetime.strftime("%Y-%m-%d %H:%M"),
                "id": item.id
            }
            for item in items
        ]
