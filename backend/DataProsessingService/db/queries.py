from sqlalchemy import select, insert

from db.database import SessionLocal, engine
from db.models import *


class DefaultDataBaseQuery:

    def __init__(self):
        self.session = SessionLocal()

    def create_all(self):
        Base.metadata.create_all(engine)

    def drop_all(self):
        Base.metadata.drop_all(bind=engine, tables=[
            DateTimeModel.__table__,
            CompositeModel.__table__,
            SatelliteModel.__table__,
            FileCompositeModel.__table__,
            FireValueModel.__table__,
        ])

    def delete_all(self):
        try:
            self.session.query(FileCompositeModel).delete()
            self.session.query(FireValueModel).delete()
            self.session.query(SatelliteModel).delete()
            self.session.query(CompositeModel).delete()
            self.session.query(DateTimeModel).delete()
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()

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
