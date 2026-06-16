import logging
from typing import List

import cv2 as cv
import numpy as np
from shapely import geometry

from api.common.point import CuttingPoint
from api.common.geotiff_rm_bg import remove_black_bg_color
from api.common.geotiff_metadata import get_metadata_from_tiff, copy_geotiff_metadata


Y = 0
X = 1


def pixel_to_geo(col, row, xy_start: tuple, pixel_size: tuple) -> tuple:
    """
    Перевод пикселей в географические координаты
    :param geo_col:
    :param geo_row:
    :param xy_start:
    :param pixel_size:
    :return tuple:
    """

    geo_col = xy_start[Y] + pixel_size[Y] * col
    geo_row = xy_start[X] - pixel_size[X] * row

    return round(geo_col, 2), round(geo_row, 2)


def geo_to_pixel(geo_col, geo_row, xy_start: tuple, pixel_size: tuple) -> tuple:
    """
    Перевод географических координат в пиксели
    :param geo_col:
    :param geo_row:
    :param xy_start:
    :param pixel_size:
    :return tuple:
    """

    col = (geo_col - xy_start[Y]) / pixel_size[Y]
    row = -1 * (geo_row - xy_start[X]) / pixel_size[X]

    return round(col, 2), round(row, 2)


def cut_polygon(path_src: str, path_dst: str, points: List[CuttingPoint]) -> None:
    """
    Выреает полигон изображения по координатам
    """

    logging.info("Cut polygon from tiff-image by geopoints")

    tiff_metadata = get_metadata_from_tiff(path_src)
    xy_start = tiff_metadata["xy_start"]
    pixel_size = tiff_metadata["pixel_size"]

    converted_points = []
    for point in points:
        col, row = geo_to_pixel(float(point.longitude), float(point.latitude), xy_start, pixel_size)
        converted_points.append((col, row))

    points_np = np.array(converted_points, np.int32)

    image = cv.imread(path_src, cv.IMREAD_UNCHANGED)
    image_height, image_width, _ = image.shape
    mask = np.zeros((image_height, image_width), dtype=np.uint8)
    cv.fillPoly(mask, [points_np], 255)

    final_image = cv.bitwise_and(image, image, mask=mask)

    final_image_x, final_image_y, final_image_width, final_image_height = cv.boundingRect(points_np)

    # удаление черного бг
    final_image = remove_black_bg_color(final_image)
    cropped_result = final_image[
         final_image_y:final_image_y+final_image_height,
         final_image_x:final_image_x+final_image_width
    ]

    cv.imwrite(path_dst, cropped_result)
    logging.info(f"Saved file: {path_dst}")
    geo_final_image_x, geo_final_image_y = pixel_to_geo(final_image_x, final_image_y, xy_start, pixel_size)

    # добавление метадаты
    model_tiepoint_tag = (0.0, 0.0, 0.0, geo_final_image_x, geo_final_image_y, 0.0)
    copy_geotiff_metadata(path_src, path_dst, model_tiepoint_tag=model_tiepoint_tag)
