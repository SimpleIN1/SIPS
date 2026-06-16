import logging
from datetime import datetime
from dataclasses import dataclass
from typing import List

from flask import url_for
from sqlalchemy import func

from api import conf
from api.db.base import db
from api.db.models import DownloadLinkModel


@dataclass
class DownloadLink:
    id: int
    link: str
    datetime_expiration: datetime


def make_link(token: str, is_add_resource=False) -> str:
    if is_add_resource:
        route = conf.ROUTES["download_by_url"] % token
    else:
        route = url_for("download_by_url", uid=token)

    return f'{conf.SCHEMA}://{conf.DOMAIN}:{conf.PORT}{route}'


class DownloadLinkService:
    def delete_link(self):
        try:
            db.session.execute(
                db.update(
                    DownloadLinkModel,
                )
                .where(
                    (func
                     .extract('day', DownloadLinkModel.datetime_expiration - datetime.now())
                     .label('days_diff') <= 0) &
                    (DownloadLinkModel.deleted == False)
                )
                .values(deleted=True)
            )
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"Session rollback {e}")

    def get_links(self, user_id: int) -> List[DownloadLink]:
        items = db.session.execute(
            db.select(
                DownloadLinkModel.id,
                DownloadLinkModel.token,
                DownloadLinkModel.datetime_expiration,
            )
            .where(
                (DownloadLinkModel.deleted == False) &
                (DownloadLinkModel.user_id == user_id)
            )
        )

        links = []
        for item in items:
            url = make_link(item.token, is_add_resource=True)
            links.append(
                DownloadLink(id=item.id, link=url,
                             datetime_expiration=item.datetime_expiration)
            )

        return links
