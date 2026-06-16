from typing import List
from dataclasses import dataclass

from shapely import geometry
from geoalchemy2.shape import from_shape
from geoalchemy2.functions import ST_Intersects
from geoalchemy2.elements import WKTElement

from api.common.composite_image import CompositeImage
from api.db.base import db
from api.common.point import CuttingPoint
from api.db.models import FileCompositeModel, CompositePolygonModel


@dataclass
class CompositeSearch:
    datetimes: List[int]
    satellites: List[int]
    composites: List[int]
    points: List[CuttingPoint] = None


def geocoords_to_polygon(points: List[CuttingPoint]) -> geometry.Polygon:
    geom = [[point.longitude, point.latitude] for point in points]
    polygon = geometry.Polygon(geom)
    return polygon


class CompositeSearchService:

    def search(self, points: List[CuttingPoint],
               datetimes: List, satellites: List[int], composites: List[int]) -> List[CompositeImage]:
        polygon = geocoords_to_polygon(points)

        items = db.session.execute(
            db.select(
                FileCompositeModel.composite_id,
                FileCompositeModel.datetime_id,
                FileCompositeModel.satellite_id
            )
            .select_from(CompositePolygonModel)
            .join(FileCompositeModel, FileCompositeModel.composite_polygon_id == CompositePolygonModel.id)
            .where(ST_Intersects(
                CompositePolygonModel.polygon, from_shape(polygon, srid=4326)) &
                   (FileCompositeModel.satellite_id.in_(satellites)) &
                   (FileCompositeModel.datetime_id.in_(datetimes)) &
                   (FileCompositeModel.composite_id.in_(composites))
                   )
        )

        composite_images = [
            CompositeImage(composite=item.composite_id,
                           satellite=item.satellite_id,
                           datetime=item.datetime_id)
            for item in items
        ]

        return composite_images
