
import cv2 as cv
import numpy as np

from utils.geotiff_metadata import copy_geotiff_metadata
from utils.geotiff_rm_bg import remove_black_bg_color


def cut_by_contour(path_src_contour: str, path_dst_contour: str, size_cut: int = 500) -> None:
    im_src_contour = cv.imread(path_src_contour)
    im_dst_contour = cv.imread(path_dst_contour)

    imgray = cv.cvtColor(im_src_contour, cv.COLOR_BGR2GRAY)

    ret, thresh = cv.threshold(imgray, 28, 255, 0)

    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    new_contours = [
        contour for contour in contours if len(contour) > size_cut
    ]

    h, w, _ = im_dst_contour.shape
    mask = np.zeros((h, w), dtype=np.uint8)
    cv.drawContours(mask, new_contours, -1, 255, thickness=cv.FILLED)
    mask_inv = cv.bitwise_not(mask)
    background_color = 0
    background = np.full_like(im_dst_contour, background_color)
    result_bg = cv.bitwise_and(background, background, mask=mask_inv)
    result_fg = cv.bitwise_and(im_dst_contour, im_dst_contour, mask=mask)

    final_image = cv.add(result_bg, result_fg)
    final_image_without_bg = remove_black_bg_color(final_image)

    cv.imwrite(path_dst_contour, final_image_without_bg)

    copy_geotiff_metadata(path_src_contour, path_dst_contour)


if __name__ == '__main__':
    path_src = '/home/grigoriy/PycharmProjects/differenttestpythonProjects/GDAL_TEST/contour-test/test/SNPP_viirs_clphs_20230617_072036_wgs84_fit.tif'
    path_dst = '/home/grigoriy/PycharmProjects/differenttestpythonProjects/GDAL_TEST/contour-test/test/SNPP_viirs_vscmo_20230617_072036_wgs84_fit.tif'
    cut_by_contour(path_src, path_dst)
