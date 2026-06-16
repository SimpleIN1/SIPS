import logging
from typing import Tuple, Any

import cv2 as cv
import numpy as np
import tifffile as tiff
from shapely import geometry
from numpy._typing import _64Bit
from numpy import ndarray, dtype, floating


Y = 0
X = 1


def pixel_to_geo(col, row, xy_start: tuple, pixel_size: tuple) -> tuple:
    geo_col = xy_start[Y] + pixel_size[Y] * col
    geo_row = xy_start[X] - pixel_size[X] * row

    return round(geo_col, 2), round(geo_row, 2)


def get_geotiff_geo_contour(path, len_points: int = 200) -> tuple[ndarray[Any, dtype[floating[_64Bit]]], ...]:
    """
    Получение контура из geotiff изображения
    :param path:
    :param len_points:
    :return:
    """

    logging.info(f"Find and fetch contour {path}")

    im = cv.imread(path)
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 28, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    new_contours = tuple(
        contour for contour in contours if len(contour) > len_points
    )

    # метаданные tiff файла
    with tiff.TiffFile(path) as tif:
        tags = tif.pages[0].tags
        model_pixel_scale_tag = tags["ModelPixelScaleTag"].value
        model_tiepoint_tag = tags["ModelTiepointTag"].value

    xy_start = model_tiepoint_tag[3], model_tiepoint_tag[4]
    pixel_size = model_pixel_scale_tag[0], model_pixel_scale_tag[1]

    geo_contours = []

    for index, cnt in enumerate(new_contours):
        cnt_reshape = cnt.reshape(1, -1, 2)
        cnt_list = cnt_reshape.tolist()
        arr = np.empty((len(cnt_list[0]), 2))

        for i, point in enumerate(cnt_list[0]):
            arr[i][X], arr[i][Y] = pixel_to_geo(point[Y], point[X], xy_start, pixel_size)

        geo_contours.append(arr)

    return tuple(geo_contours)


def geotiff_to_polygon(contours: tuple[ndarray[Any, dtype[floating[_64Bit]]], ...]):
    """
    Преобразование контуров в полигон
    :param contours:
    :return:
    """

    logging.info("Convert to MultiPolygon")
    polygons = []
    for contour in contours:
        polygons.append(geometry.Polygon(contour))

    multi_polygon = geometry.MultiPolygon(polygons)
    return multi_polygon
