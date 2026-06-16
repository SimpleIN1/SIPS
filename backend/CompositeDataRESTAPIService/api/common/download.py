from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from api import conf
from api.db.base import db
from api.db.models import UserFileCompositeModel, FileCompositeModel, DownloadLinkModel, DownloadHistoryModel


@dataclass
class DownloadItem:
    download_link_id: int
    filename: str


class DownloadService:
    def get_filename(self, uid: str, user_id: int = None) -> DownloadItem | None:

        q1 = db.select(
                DownloadLinkModel.id,
                UserFileCompositeModel.filename,
            ) \
            .select_from(DownloadLinkModel) \
            .join(UserFileCompositeModel, UserFileCompositeModel.id == DownloadLinkModel.user_file_composite_id) \
            .where(
                (DownloadLinkModel.deleted == False) &
                (DownloadLinkModel.token == uid)
            )

        q2 = db.select(
                DownloadLinkModel.id,
                FileCompositeModel.filename,
            )\
            .select_from(DownloadLinkModel) \
            .join(FileCompositeModel, FileCompositeModel.id == DownloadLinkModel.file_composite_id) \
            .where(
                (DownloadLinkModel.deleted == False) &
                (DownloadLinkModel.token == uid)
            )

        q3 = db.union(q1, q2)

        items = db.session.execute(
            q3
        )
        items = list(items)

        if not items:
            return None

        item = items[0]

        return DownloadItem(
            download_link_id=item.id,
            filename=item.filename
        )

    def check_download_file_length(self, user_id: int) -> bool:
        items = db.session.execute(
            db.select(
                DownloadHistoryModel.id
            )
            .where(
                (DownloadHistoryModel.user_id == user_id) &
                (db.func.to_char(DownloadHistoryModel.datetime_created, "YYYY-MM-DD") == str(date.today()))
            )
        )

        if len(list(items)) > conf.COUNT_DOWNLOAD_DAYS:
            return False

        return True
