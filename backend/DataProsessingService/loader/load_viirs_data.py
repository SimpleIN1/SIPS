import os
import shutil
import logging
from pathlib import Path
from datetime import datetime

from geoalchemy2.shape import from_shape

import conf
from db.models import composite_data, composite
from db.queries import DefaultDataBaseQuery, CompositeDataBaseQuery, CompositeDataDataBaseQuery
from utils.geotiff_contour import get_geotiff_geo_contour, geotiff_to_polygon
from utils.mkdir import make_directory

confirm_all = False

# Для одной базы
composite_dbq = CompositeDataBaseQuery()

# Дл второй базы
composite_data_dbq = CompositeDataDataBaseQuery()


def format_date_time(date_time: str, format: str):
    datetime_fixed = datetime.strptime(
        f"{date_time}",
        f"{format}"
    )
    return datetime_fixed


def get_and_create_composites():
    logging.info("Perform get and create composites")

    tmp_composite_names = {item.name for item in composite_dbq.get_all(composite.CompositeModel)}
    res = set(conf.COMPOSITE_NAMES).difference(tmp_composite_names)
    if res:
        composites = []
        for name in res:
            composites.append(composite.CompositeModel(name=name))
        composite_dbq.bulk_insert_2(composites)

    composite_obj = {item.name: item.id for item in composite_dbq.get_all(composite.CompositeModel)}
    return composite_obj


def get_and_create_satellites():
    logging.info("Perform get and create satellites")

    tmp_satellite_tags = {item.tag for item in composite_dbq.get_all(composite.SatelliteModel)}
    satellite_tags = set(conf.SATELLITES.keys())
    res = set(satellite_tags).difference(tmp_satellite_tags)
    if res:
        satellites = []
        for tag in res:
            satellites.append(composite.SatelliteModel(tag=tag, name=conf.SATELLITES[tag]))
        composite_dbq.bulk_insert_2(satellites)

    satellites_obj = {item.tag: item.id for item in composite_dbq.get_all(composite.SatelliteModel)}
    return satellites_obj


def create_composite_files(
        composite_files: dict,
        composite_names: dict,
        path_save: str,
        satellite_id: int,
        datetime_id: int
):
    logging.info("Perform create composite files")
    composite_model_files = []
    composite_data_model_files = []

    filename = composite_files["clphs"]
    contours = get_geotiff_geo_contour(filename)
    polygon = geotiff_to_polygon(contours)

    instance_polygon = composite_data_dbq.insert_data(
        composite_data.CompositePolygonModel(polygon=from_shape(polygon))
    )

    for composite_name, filename in composite_files.items():

        base_filename = os.path.basename(filename)
        name = os.path.join(path_save, base_filename)

        item = composite.FileCompositeModel(
            filename=name,
            is_downloadable_tiles=True,
            datetime_created=datetime.now(),
            datetime_id=datetime_id,
            composite_id=composite_names[composite_name],
            satellite_id=satellite_id,
        )
        composite_model_files.append(item)

        ###  Запись в composite_data_dbq
        item1 = composite_data.FileCompositeModel(
            filename=name,
            is_downloadable_tiles=True,
            datetime_created=datetime.now(),
            datetime_id=datetime_id,
            composite_id=composite_names[composite_name],
            satellite_id=satellite_id,
            composite_polygon_id=instance_polygon.id,
        )
        composite_data_model_files.append(item1)

        ###

    composite_dbq.bulk_insert_2(composite_model_files)
    composite_data_dbq.bulk_insert_2(composite_data_model_files)


def fetch_datetime_satellite(gitco_filename_data: list) -> tuple:
    gitco_filename_data.sort()
    gitco_filename_first = gitco_filename_data[0][-2:]
    datetime_formatted = format_date_time(" ".join(gitco_filename_first), "%Y%m%d %H%M")
    satellite = gitco_filename_data[0][0]
    return datetime_formatted, satellite


def get_or_create_datetime(datetime_formatted) -> composite.DateTimeModel:
    logging.info("Perform get or create datetime")

    datetime_obj = composite_dbq.get_object_or_none(composite.DateTimeModel, datetime=datetime_formatted)
    if not datetime_obj:
        datetime_obj = composite_dbq.insert_data(
            composite.DateTimeModel(datetime=datetime_formatted)
        )

    return datetime_obj


def read_fire_values(fire_value_filenames: list, satellite_id: int, datetime_id: int):
    logging.info("Perform read fire values")

    fire_values = []
    for item in fire_value_filenames:
        with open(item['filename'], 'r') as f:
            for line in f.readlines():
                line = line.rstrip('\n')
                latitude, longitude, temperature, *_ = line.split(',')
                fire_value = composite.FireValueModel(
                    longitude=longitude,
                    latitude=latitude,
                    temperature=temperature,
                    resolution=composite.FireValueModel.RESOLUTION_SATELLITE[item["type"]],
                    satellite_id=satellite_id,
                    datetime_id=datetime_id
                )
                fire_values.append(fire_value)

    composite_dbq.bulk_insert_2(fire_values)


def check_add_data(composite_filenames,
                   fire_value_filenames: list,
                   satellite: str,
                   datetime_formatted) -> bool:
    global confirm_all
    print("-: Composite filenames".upper())
    for composite_name, filename in composite_filenames.items():
        print(f"{filename}, {composite_name}")

    datetime_obj = composite_dbq.get_object_or_none(composite.DateTimeModel, datetime=datetime_formatted)
    if datetime_obj:
        print("-----")
        print(f"{datetime_formatted} is exists into DataBase.")

        items = list(composite_dbq.get_all_by_filter(composite.FileCompositeModel, datetime_id=datetime_obj.id))
        print(f"Count file composite model items: {len(items)}, by datetime: {datetime_formatted}")
        for item in items:
            print(item.filename)

    print("-: Fire value filenames".upper())
    for item in fire_value_filenames:
        print(f"{item['filename']}, {item['type']}")

    while answer := str(input(f"Are you continue? y/n/a/s/d(delete all) \n "
                              f"y - confirm current. \n "
                              f"n - dont confirm current. \n "
                              f"a - confirm all. \n "
                              f"s - stop. \n "
                              f"d - delete all.\n"
                              f"-> ")):
        if answer.upper() == 'Y':
            return True
        elif answer.upper() == 'N':
            return False
        elif answer.upper() == 'A':
            confirm_all = True
            return True
        elif answer.upper() == 'S':
            exit(0)
        elif answer.upper() == 'D':
            composite_dbq.delete_all()
            composite_data_dbq.delete_all()
            exit(0)


def make_path_save(satellite: str, datetime_formatted: datetime):
    date, time = datetime_formatted.strftime("%Y%m%d %H%M").split(' ')
    path = f"{conf.PATH_TO_TIF_DIRS}/{satellite}/{date}/{time}"
    make_directory(path)

    return path


def copy_file_to_tif_dir(composite_filenames: dict, path_save: str):
    for _, filename in composite_filenames.items():
        filename = os.path.basename(filename)
        dst_path = f"{path_save}/{filename}"
        if not os.path.exists(dst_path):
            shutil.copy(filename, dst_path)


def main():
    composite_names = get_and_create_composites()
    satellites = get_and_create_satellites()

    composite_filenames = {}
    fire_value_filenames = []
    gitco_filename_data = []

    with open(conf.PATH_TO_FILE_DIRS, 'r') as f:
        for path in f.readlines():
            path = path.rstrip('\n')

            gitco_filename_data.clear()
            fire_value_filenames.clear()
            composite_filenames.clear()

            for filename in os.listdir(path):
                if match := conf.pattern_composite.search(filename):
                    composite_filenames[match.groups()[0]] = f"{path}/{filename}"
                elif match := conf.pattern_v375m_v750m_fire_value.search(filename):
                    type_fv = conf.TYPE_FIRE_VALUE[match.groups()[0]]
                    fire_value_filenames.append({"filename": f"{path}/{filename}", "type": type_fv})
                elif match := conf.pattern_GITCO.search(filename):
                    gitco_filename_data.append(match.groups())

            datetime_formatted, satellite = fetch_datetime_satellite(gitco_filename_data)
            satellite_id = satellites[conf.SATELLITE_TAGS[satellite]]

            path_save = make_path_save(conf.SATELLITE_TAGS[satellite], datetime_formatted)
            #
            if not confirm_all:
                if not check_add_data(composite_filenames, fire_value_filenames, satellite, datetime_formatted):
                    continue

            datetime_obj = get_or_create_datetime(datetime_formatted)

            read_fire_values(fire_value_filenames, satellite_id, datetime_obj.id)

            # copeing
            copy_file_to_tif_dir(composite_filenames, path_save)

            create_composite_files(composite_filenames, composite_names, path_save, satellite_id, datetime_obj.id)


if __name__ == '__main__':
    main()
