from sqlalchemy import Integer, String, DateTime, ForeignKey, Numeric, Boolean, SmallInteger, Column
from geoalchemy2 import Geometry
from sqlalchemy.orm import Mapped, mapped_column
from db.database import composite_data_pbase


Base = composite_data_pbase.Base


class CompositePolygonModel(Base):
    """
    Stores polygon snapshots
    """

    __tablename__ = "composite_polygon"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    polygon = Column(Geometry("MultiPolygon", srid=4326))

    def __repr__(self):
        return f"<CompositePolygon {self.id}>"


class FileCompositeModel(Base):
    """
    Stores snapshots
    """

    __tablename__ = "file_composite"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)

    filename: Mapped[str] = mapped_column(String)
    is_downloadable_tiles: Mapped[bool] = mapped_column(Boolean, default=False)

    composite_polygon_id = mapped_column(Integer,
                                         ForeignKey(f'{CompositePolygonModel.__tablename__}.id'), nullable=False)

    datetime_id: Mapped[int] = mapped_column(Integer)
    composite_id: Mapped[int] = mapped_column(Integer)
    satellite_id: Mapped[int] = mapped_column(Integer)

    datetime_created: Mapped[DateTime] = mapped_column(DateTime(timezone=False))

    def __repr__(self):
        return f"<FileComposite {self.id}>"


class UserFileCompositeModel(Base):
    """
    Stores user snapshots of polygons
    """

    __tablename__ = "user_file_composite"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    file_composite_id: Mapped[str] = mapped_column(Integer, ForeignKey(f'{FileCompositeModel.__tablename__}.id'))
    filename: Mapped[str] = mapped_column(String)
    polygon = Column(Geometry("POLYGON"))
    datetime_expiration: Mapped[DateTime] = mapped_column(DateTime(timezone=False))
    datetime_created: Mapped[DateTime] = mapped_column(DateTime(timezone=False))
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"<UserFileComposite {self.uid}>"


class DownloadLinkModel(Base):
    """
    Stores the user's download links
    """

    __tablename__ = "download_link"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    token: Mapped[str] = mapped_column(String, unique=True)
    file_composite_id: Mapped[str] = mapped_column(
        Integer, ForeignKey(f'{FileCompositeModel.__tablename__}.id'), nullable=True)
    user_file_composite_id: Mapped[str] = mapped_column(
        Integer, ForeignKey(f'{UserFileCompositeModel.__tablename__}.id'), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer)
    datetime_expiration: Mapped[DateTime] = mapped_column(DateTime(timezone=False))
    datetime_created: Mapped[DateTime] = mapped_column(DateTime(timezone=False))
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"<DownloadLink {self.id}>"


class DownloadHistoryModel(Base):
    """
    Stores the user's download history
    """

    __tablename__ = "download_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(Integer)
    download_link_id: Mapped[str] = mapped_column(Integer, ForeignKey(f'{DownloadLinkModel.__tablename__}.id'))
    datetime_created: Mapped[DateTime] = mapped_column(DateTime(timezone=False))

    def __repr__(self):
        return f"<DownloadHistory {self.id}>"
