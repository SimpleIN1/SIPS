from typing import List

from sqlalchemy import insert, func, delete, select

from api.db.base import db, Base, engine, SessionLocal
# from api.db import models as m


# class FileDownloadDB:
#     def get_by_uid(self, uid):
#         instance = db.get_or_404(
#             m.DownloadHistoryModel, uid, description="Composite (image for download) not found!"
#         )
#         return instance
#
#     def load_urls_downloading(self, items: list):
#         try:
#             db.session.bulk_save_objects(items)
#             db.session.commit()
#         except:
#             db.session.rollback()
#             return False
#         return True
#
#     def get_count_files_to_download_by_user(self, user_id) -> int:
#         count = db.session.execute(
#             db.select(func.count(m.DownloadHistoryModel.user_id))
#             .where(m.DownloadHistoryModel.user_id == user_id)
#         ).scalar()
#         return count
#
#     def delete_all(self):
#         db.session.execute(
#             delete(m.DownloadHistoryModel)
#         )
#         db.session.commit()


# class UserFileDownloadDB:
#     def get_count_downloaded_files_by_user(self, user_id) -> int:
#         count = db.session.execute(
#             db.select(func.count(m.UserFileDownloadModel.user_id))
#             .where(m.UserFileDownloadModel.user_id == user_id)
#         ).scalar()
#         return count
#
#     def insert_user_file_download_obj(self, item: m.UserFileDownloadModel):
#         db.session.add(item)
#         db.session.commit()
#
#     def delete_all(self):
#         db.session.execute(
#             delete(m.UserFileDownloadModel)
#         )
#         db.session.commit()
#
#
# class FileCompositeDB:
#     def get(self, images: list):
#         condition = None
#         for index, image in enumerate(images):
#             tmp = (
#                 (m.CompositeModel.name == image.composite) &
#                 (m.SatelliteModel.tag == image.satellite) &
#                 (m.DateTimeModel.datetime == image.datetime)
#             )
#             condition = tmp if index == 0 else condition | tmp
#
#         items = db.session.execute(
#             db.select(
#                 m.FileCompositeModel, m.DateTimeModel, m.SatelliteModel, m.CompositeModel
#             )
#             .join(
#                 m.SatelliteModel,
#                 m.FileCompositeModel.satellite_id == m.SatelliteModel.id
#             )
#             .join(
#                 m.DateTimeModel,
#                 m.FileCompositeModel.datetime_id == m.DateTimeModel.id
#             )
#             .join(
#                 m.CompositeModel,
#                 m.FileCompositeModel.composite_id == m.CompositeModel.id
#             )
#             .where(condition)
#             # .order_by(m.DateTimeModel.datetime, m.CompositeModel.name, m.SatelliteModel.tag)
#         ).all()
#
#         return items


class DefaultDataBaseQuery:
    session = None
    base = None
    engine = None

    def __init__(self):
        if not self.session:
            raise Exception("Session is empty")
        if not self.base:
            raise Exception("Base is empty")
        if not self.engine:
            raise Exception("Engine is empty")

    def drop_all(self):
        raise NotImplementedError()

    def delete_all(self):
        raise NotImplementedError()

    def get_or_create(self, model, **kwargs):

        instance = self.session.query(model).filter_by(**kwargs).one_or_none()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            self.session.add(instance)
            self.session.commit()
            return instance

    def get_object_or_none(self, model, **kwargs):
        instance = self.session.query(model).filter_by(**kwargs).one_or_none()
        return instance

    def get_all_by_filter(self, model, **kwargs):
        query = select(model).filter_by(**kwargs)
        queryset = self.session.scalars(query)
        return queryset

    def get_all(self, model):
        query = select(model)
        queryset = self.session.scalars(query)
        return queryset

    def insert_data(self, instance, flush=False):
        self.session.add(instance)
        if not flush:
            self.session.commit()
        else:
            self.session.flush()
        return instance

    def bulk_insert(self, model, items: list):
        self.session.execute(insert(model), items)
        self.session.commit()

    def bulk_insert_2(self, items: list):
        self.session.add_all(items)
        self.session.commit()
        return items

    def bulk_insert_scalars(self, model, items: list):
        output_items = self.session.scalars(insert(model).returning(model), items)
        self.session.commit()
        return output_items


class CompositeDataDataBaseQuery(DefaultDataBaseQuery):
    session = SessionLocal()
    engine = engine
    base = Base
