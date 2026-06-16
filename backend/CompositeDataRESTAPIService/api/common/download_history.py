import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List

from api.common.pagination import paginate, Pagination
from api.db.base import db
from api.db.models import DownloadLinkModel, DownloadHistoryModel, UserFileCompositeModel, FileCompositeModel
from api.db.requests import CompositeDataDataBaseQuery


cddbq = CompositeDataDataBaseQuery()


@dataclass
class DownloadHistoryCreated:
    user_id: int
    download_link_id: int


@dataclass
class DownloadHistory:
    id: int
    datetime_download: datetime
    datetime_composite: int
    satellite: int
    composite: int
    is_object_cut: bool


class DownloadHistoryService:
    def create(self, dh_item: DownloadHistoryCreated, cddbq_user: CompositeDataDataBaseQuery = None):
        logging.info("Add download history")

        cddbq1 = cddbq_user or cddbq
        flush = bool(cddbq_user)

        dh_instance = DownloadHistoryModel(
            user_id=dh_item.user_id,
            download_link_id=dh_item.download_link_id,
            datetime_created=datetime.now(),
        )
        cddbq1.insert_data(dh_instance, flush=flush)

    def list(self, page: int, per_page: int, user_id: int) -> Pagination:
        q1 = db.select(
                DownloadHistoryModel.id.label("download_id"),
                DownloadHistoryModel.datetime_created.label("datetime_download"),
                FileCompositeModel.satellite_id.label("satellite"),
                FileCompositeModel.composite_id.label("composite"),
                FileCompositeModel.datetime_id.label("datetime_composite"),
                DownloadLinkModel.user_file_composite_id,
                DownloadLinkModel.file_composite_id,
            ) \
            .join(DownloadHistoryModel, DownloadLinkModel.id == DownloadHistoryModel.download_link_id) \
            .join(UserFileCompositeModel, UserFileCompositeModel.id == DownloadLinkModel.user_file_composite_id) \
            .join(FileCompositeModel, UserFileCompositeModel.file_composite_id == FileCompositeModel.id) \
            .where(
                (DownloadHistoryModel.user_id == user_id)
            )

        q2 = db.select(
                DownloadHistoryModel.id.label("download_id"),
                DownloadHistoryModel.datetime_created.label("datetime_download"),
                FileCompositeModel.satellite_id.label("satellite"),
                FileCompositeModel.composite_id.label("composite"),
                FileCompositeModel.datetime_id.label("datetime_composite"),
                DownloadLinkModel.user_file_composite_id,
                DownloadLinkModel.file_composite_id,
            )\
            .select_from(DownloadLinkModel) \
            .join(DownloadHistoryModel, DownloadLinkModel.id == DownloadHistoryModel.download_link_id) \
            .join(FileCompositeModel, FileCompositeModel.id == DownloadLinkModel.file_composite_id) \
            .where(
                (DownloadHistoryModel.user_id == user_id)
            )

        q3 = db.union(q1, q2)

        pagination = paginate(
            q3,
            page=page,
            per_page=per_page,
        )

        dh_items = []
        for item in pagination.items:
            is_object_cut = bool(item.user_file_composite_id) or False

            dh_items.append(
                DownloadHistory(
                    id=item.download_id, datetime_download=item.datetime_download,
                    datetime_composite=item.datetime_composite, satellite=item.satellite,
                    composite=item.composite, is_object_cut=is_object_cut
                )
            )
        pagination.items = dh_items
        return pagination


