from sqlalchemy import Integer, String, DateTime, ForeignKey, Numeric, Boolean, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from api.db.base import db, Base


class DateTimeModel(db.Model):
    """
    Stores date and time of snapshot.
    """

    __tablename__ = "date_time"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=False), unique=True)


class CompositeModel(db.Model):
    """
    Stores the tags of composite.
    """

    __tablename__ = "composite"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)


class SatelliteModel(db.Model):
    """
    Stores the satellite name and tag.
    """

    __tablename__ = "satellite"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)

    name: Mapped[str] = mapped_column(String(30))
    tag: Mapped[str] = mapped_column(String(20), unique=True)


class FileCompositeModel(db.Model):
    """
    Stores snapshots.
    """

    __tablename__ = "file_composite"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)

    filename: Mapped[str] = mapped_column(String)
    is_downloadable_tiles: Mapped[bool] = mapped_column(Boolean, default=False)

    datetime_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DateTimeModel.__tablename__}.id'))
    composite_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{CompositeModel.__tablename__}.id'))
    satellite_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{SatelliteModel.__tablename__}.id'))

    datetime_created: Mapped[DateTime] = mapped_column(DateTime(timezone=False))


class FireValueModel(db.Model):  # cache
    """
    Stores fire value.
    """

    __tablename__ = "fire_value"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)

    temperature: Mapped[float] = mapped_column(Numeric(5, 2))
    longitude: Mapped[float] = mapped_column(Numeric(8, 5))
    latitude: Mapped[float] = mapped_column(Numeric(8, 5))
    resolution: Mapped[int] = mapped_column(SmallInteger, default=1)

    satellite_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{SatelliteModel.__tablename__}.id'))
    datetime_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DateTimeModel.__tablename__}.id'))

    def __repr__(self):
        return f"<FireValue {self.id}>"

    RESOLUTION_SATELLITE = {
        "375m": 1,
        "750m": 2
    }
