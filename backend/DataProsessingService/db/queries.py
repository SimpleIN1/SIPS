from sqlalchemy import select, insert

from db.models import composite, composite_data
from db.database import composite_pbase, composite_data_pbase


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

    def insert_data(self, instance):
        self.session.add(instance)
        self.session.commit()
        return instance

    def bulk_insert(self, model, items: list):
        self.session.execute(insert(model), items)
        self.session.commit()

    def bulk_insert_2(self, items: list):
        self.session.add_all(items)
        self.session.commit()

    def bulk_insert_scalars(self, model, items: list):
        output_items = self.session.scalars(insert(model).returning(model), items)
        self.session.commit()
        return output_items


class CompositeDataBaseQuery(DefaultDataBaseQuery):
    session = composite_pbase.SessionLocal()
    engine = composite_pbase.engine
    base = composite_pbase.Base

    def drop_all(self):
        self.base.metadata.drop_all(bind=self.engine, tables=[
            composite.DateTimeModel.__table__,
            composite.CompositeModel.__table__,
            composite.SatelliteModel.__table__,
            composite.FileCompositeModel.__table__,
            composite.FireValueModel.__table__,
        ])

    def delete_all(self):
        try:
            self.session.query(composite.FileCompositeModel).delete()
            self.session.query(composite.FireValueModel).delete()
            self.session.query(composite.SatelliteModel).delete()
            self.session.query(composite.CompositeModel).delete()
            self.session.query(composite.DateTimeModel).delete()
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()


class CompositeDataDataBaseQuery(DefaultDataBaseQuery):
    session = composite_data_pbase.SessionLocal()
    engine = composite_data_pbase.engine
    base = composite_data_pbase.Base

    def drop_all(self):
        self.base.metadata.drop_all(bind=self.engine, tables=[
            composite_data.DownloadHistoryModel.__table__,
            composite_data.DownloadLinkModel.__table__,
            composite_data.UserFileCompositeModel.__table__,
            composite_data.FileCompositeModel.__table__,
            composite_data.CompositePolygonModel.__table__
        ])

    def delete_all(self):
        try:
            self.session.query(composite_data.UserFileCompositeModel).delete()
            self.session.query(composite_data.DownloadHistoryModel).delete()
            self.session.query(composite_data.FileCompositeModel).delete()
            self.session.query(composite_data.CompositePolygonModel).delete()
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()

