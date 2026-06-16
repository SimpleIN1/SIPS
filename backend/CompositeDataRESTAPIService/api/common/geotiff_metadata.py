import logging

import tifffile as tiff
from enum import Enum


metadata_attrs = [
    "ModelPixelScaleTag", "ModelTiepointTag",
    "GeoKeyDirectoryTag", "GeoDoubleParamsTag", "GeoAsciiParamsTag", "Compression", "ColorMap"
]


def copy_geotiff_metadata(path_src_geo, path_dst_geo, **kwargs) -> None:
    """
    Копирование гео-данных одного tiff-изображения в другое
    :param path_src_geo:
    :param path_dst_geo:
    :param kwargs:
    :return:
    """

    logging.info("Copy geodata from tiff-image")
    metadata = {}

    with tiff.TiffFile(path_src_geo) as tif:

        for attr in metadata_attrs:
            value = tif.pages[0].tags[attr].value
            if isinstance(value, Enum):
                value = value.value
            metadata[attr] = value

    model_tiepoint_tag = kwargs.get("model_tiepoint_tag")
    if model_tiepoint_tag:
        metadata["ModelTiepointTag"] = model_tiepoint_tag

    extratags = [
        (33550, 'd', len(metadata["ModelPixelScaleTag"]), metadata["ModelPixelScaleTag"], True),
        (33922, 'd', len(metadata["ModelTiepointTag"]), metadata["ModelTiepointTag"], True),
        (34735, 'H', len(metadata["GeoKeyDirectoryTag"]), metadata["GeoKeyDirectoryTag"], True),
        (34736, 'd', len(metadata["GeoDoubleParamsTag"]), metadata["GeoDoubleParamsTag"], True),
        (34737, 's', len(metadata["GeoAsciiParamsTag"]), metadata["GeoAsciiParamsTag"], True)
    ]

    image_dst_geo = tiff.imread(path_dst_geo)

    tiff.imwrite(
        path_dst_geo,
        image_dst_geo,
        compression=metadata["Compression"],
        extratags=extratags,
    )


def print_geotiff_metadata(path):
    """
    Вывод метадаты для файла
    :param path:
    :return:
    """

    logging.info(f"#Print metadata for: {path}#")
    with tiff.TiffFile(path) as tif:
        # Читаем метаданные первой страницы (Image File Directory)
        for tag in tif.pages[0].tags.values():
            tag_name, tag_value = tag.name, tag.value
            if tag_name in metadata_attrs:
                print(f"{tag_name}: {tag_value}")


def get_metadata_from_tiff(path: str) -> dict:
    """
    Извлечение метаданных из tiff-изображения
    :param path:
    :return:
    """

    logging.info("Fetchin metadata from tif-iamge")
    # метаданные tiff файла
    with tiff.TiffFile(path) as tif:
        tags = tif.pages[0].tags
        model_pixel_scale_tag = tags["ModelPixelScaleTag"].value
        model_tiepoint_tag = tags["ModelTiepointTag"].value

    xy_start = model_tiepoint_tag[3], model_tiepoint_tag[4]
    pixel_size = model_pixel_scale_tag[0], model_pixel_scale_tag[1]

    return {
        "xy_start": xy_start,
        "pixel_size": pixel_size
    }
