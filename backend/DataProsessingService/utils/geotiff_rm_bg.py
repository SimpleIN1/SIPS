import logging
import cv2 as cv


def remove_black_bg_color(image):
    """
    Удаление черного цвета
    :param image:
    :return:
    """

    logging.info("Remove bg color")

    if image.shape[2] == 3:
        image = cv.cvtColor(image, cv.COLOR_BGR2BGRA)

    black_pixels = (image[:, :, 0] == 0) & (image[:, :, 1] == 0) & (image[:, :, 2] == 0)
    image[black_pixels, 3] = 0

    return image
