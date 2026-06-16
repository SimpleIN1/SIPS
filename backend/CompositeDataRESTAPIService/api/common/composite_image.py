from typing import List
from dataclasses import dataclass
from datetime import datetime, date

from api import conf
from api.db.base import db
from api.common.point import CuttingPoint
from api.db.models import FileCompositeModel, CompositePolygonModel, UserFileCompositeModel


@dataclass
class CompositeImage:
    datetime: int
    satellite: int
    composite: int


@dataclass
class CompositeTask:
    points: List[CuttingPoint]
    images: List[CompositeImage]


@dataclass
class CompositeTaskContainer:
    points: List[CuttingPoint]
    images: List[CompositeImage]
    user_id: int
    email: str


@dataclass
class FileComposite:
    id: int
    datetime: int
    satellite: int
    composite: int
    filename: str = None


class CompositeCutService:
    def get_composites(self, datetimes, composites, satellites) -> List[FileComposite]:
        items = db.session.execute(
            db.select(
                FileCompositeModel.id,
                FileCompositeModel.filename,
                FileCompositeModel.datetime_id,
                FileCompositeModel.satellite_id,
                FileCompositeModel.composite_id,
            )
            .where(
                (FileCompositeModel.satellite_id.in_(satellites)) &
                (FileCompositeModel.datetime_id.in_(datetimes)) &
                (FileCompositeModel.composite_id.in_(composites))
            )
        )

        return [
            FileComposite(
                id=item.id,
                filename=item.filename,
                datetime=item.datetime_id,
                composite=item.composite_id,
                satellite=item.satellite_id,
            )
            for item in items
        ]

    def check_length_carved_images(self, images, user_id) -> bool:

        items = db.session.execute(
            db.select(
                UserFileCompositeModel.id
            )
            .where(
                (UserFileCompositeModel.user_id == user_id) &
                (db.func.to_char(UserFileCompositeModel.datetime_created, "YYYY-MM-DD") == str(date.today()))
            )
        )

        if len(list(items)) + len(images) >= conf.COUNT_TASK_CUT_DAYS:
            return False

        return True
