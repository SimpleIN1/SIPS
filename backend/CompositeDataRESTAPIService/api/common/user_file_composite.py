import logging
import os.path
import shutil
from datetime import datetime
from dataclasses import dataclass

from sqlalchemy import func

from api import conf
from api.db.base import db
from api.db.models import UserFileCompositeModel


class UserFileCompositeService:
    def delete_expiration_files(self):
        try:
            items = db.session.execute(
                db.select(
                    UserFileCompositeModel.id,
                    UserFileCompositeModel.filename,
                )
                .where(
                    (func
                    .extract('day', UserFileCompositeModel.datetime_expiration - datetime.now())
                    .label('days_diff') <= 0) &
                    (UserFileCompositeModel.deleted == False)
                )
            )
            ufs_items = list(items)

            db.session.execute(
                db.update(
                    UserFileCompositeModel,
                )
                .where(
                    UserFileCompositeModel.id.in_([item.id for item in ufs_items])
                )
                .values(deleted=True)
            )
            db.session.commit()

            for item in ufs_items:
                image_dir = os.path.dirname(item.filename)
                if os.path.exists(image_dir):
                    shutil.rmtree(image_dir)

        except Exception as e:
            db.session.rollback()
            logging.error(f"Session rollback {e}")
