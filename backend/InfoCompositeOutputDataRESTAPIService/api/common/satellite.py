from api.db.base import db
from api.db.models import SatelliteModel


def get_satellites():
    return db.session.execute(db.select(SatelliteModel)).scalars()


def get_satellite_by_id(id):
    return db.get_or_404(SatelliteModel, id)
