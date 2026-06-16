import logging
from typing import List
from datetime import datetime, timedelta, date
from dataclasses import dataclass

from api import conf
from api.common.code_generator import generate_sequence
from api.common.download_link import DownloadLink, make_link
from api.db.base import db
from api.db.models import FileCompositeModel, DownloadLinkModel
from api.common.composite_image import CompositeImage
from api.db.requests import CompositeDataDataBaseQuery


cddbq = CompositeDataDataBaseQuery()


@dataclass
class CompositeGenerateLink:
    images: List[CompositeImage]


@dataclass
class CompositeGenerateLinkContainer:
    images: List[CompositeImage]
    user_id: int


class GenerateLinkService:
    def create_links(self, composite_item: CompositeGenerateLinkContainer) -> List[DownloadLink]:

        datetimes = [item.datetime for item in composite_item.images]
        composites = [item.composite for item in composite_item.images]
        satellites = [item.satellite for item in composite_item.images]

        items = db.session.execute(
            db.select(
                FileCompositeModel.id
            )
            .where(
                (FileCompositeModel.satellite_id.in_(satellites)) &
                (FileCompositeModel.datetime_id.in_(datetimes)) &
                (FileCompositeModel.composite_id.in_(composites))
            )
        )

        dl_items = []
        try:
            for item in items:
                datetime_now = datetime.now()
                dl_items.append(
                    DownloadLinkModel(
                        token=generate_sequence(),
                        file_composite_id=item.id,
                        user_file_composite_id=None,
                        user_id=composite_item.user_id,
                        datetime_expiration=datetime_now + timedelta(days=conf.DAYS_STORED),
                        datetime_created=datetime_now
                    )
                )
            dl_items = cddbq.bulk_insert_2(dl_items)

            return [DownloadLink(id=item.id,
                                 link=make_link(token=item.token, is_add_resource=True),
                                 datetime_expiration=item.datetime_expiration) for item in dl_items]
        except Exception as e:
            cddbq.session.rollback()
            logging.error(f"Session rollback {e}")

    def check_generated_links_length(self, user_id: int) -> bool:
        items = db.session.execute(
            db.select(
                DownloadLinkModel.id
            )
            .where(
                (DownloadLinkModel.user_id == user_id) &
                (db.func.to_char(DownloadLinkModel.datetime_created, "YYYY-MM-DD") == str(date.today()))
            )
        )
        if len(list(items))+1 > conf.COUNT_DOWNLOAD_LINK_DAYS:
            return False

        return True

