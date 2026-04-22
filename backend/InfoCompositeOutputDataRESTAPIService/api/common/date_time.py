from sqlalchemy import func

from api.common.input_params import InputParams
from api.db.base import db
from api.db.models import DateTimeModel


class DateService:
    def get_dates(self):
        items = db.session.execute(db.select(DateTimeModel.datetime))
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
            tmp = str(item.datetime.date())
            year, month, day = tmp.split('-')
            tmp_dict.setdefault(year, {})
            tmp_dict[year].setdefault(month, [])
            tmp_dict[year][month].append(tmp)

        return {"dates": tmp_dict}


class DateTime(InputParams):
    def get_datetimes(self):
        datetimes = db.session.execute(
            db.select(DateTimeModel).where(func.to_char(DateTimeModel.datetime, "YYYY-MM-DD") == self.date)
        ).scalars()

        return datetimes

    def fetch_times(self, items):
        return [item.datetime.strftime("%H:%M") for item in items]
