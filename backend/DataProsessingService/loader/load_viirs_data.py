import os
import re
import pprint
import logging
from pathlib import Path
from datetime import datetime

import shutil
import conf
from db.models import *
from db.queries import DefaultDataBaseQuery


SATELLITES = {
    "snpp": "Soumi NPP",
    "noaa20": "NOAA-20"
}
SATELLITE_TAGS = {
    "npp": "snpp",
    "snpp": "snpp",
    "j01": "noaa20",
    "noaa20": "noaa20",
}
COMPOSITE_NAMES = (
    "aot550", "aotaps", "clmsk", "clmsk2", "clphs",
    "frmsk", "vievi", "vindvi", "vlst", "vscmo",
)
TYPE_FIRE_VALUE = {
    "VF375": "375m",
    "FL": "750m"
}

confirm_all = False

regex = r"viirs_([a-z\d]+)_"
pattern_composite = re.compile(regex)

regex_datetime = r"d(\d{8})_t(\d{4})"
pattern_datetime = re.compile(regex_datetime)

regex_v375m_v750m_fire_value = r"^(VF375|FL).+\.txt$"
pattern_v375m_v750m_fire_value = re.compile(regex_v375m_v750m_fire_value)

regex_GITCO = r"^GITCO_(\w+)_d(\d{8})_t(\d{4}).+\.h5$"
pattern_GITCO = re.compile(regex_GITCO)


def format_date_time(date_time: str, format: str):
    datetime_fixed = datetime.strptime(
        f"{date_time}",
        f"{format}"
    )
    return datetime_fixed


def get_and_create_composites(dbbq: DefaultDataBaseQuery):
    logging.info("Perform get and create composites")

    tmp_composite_names = {item.name for item in dbbq.get_all(CompositeModel)}
    res = set(COMPOSITE_NAMES).difference(tmp_composite_names)
    if res:
        composites = []
        for name in res:
            composites.append(CompositeModel(name=name))
        dbbq.bulk_insert_2(composites)

    composite_obj = {item.name: item.id for item in dbbq.get_all(CompositeModel)}
    return composite_obj


def get_and_create_satellites(dbbq: DefaultDataBaseQuery):
    logging.info("Perform get and create satellites")

    tmp_satellite_tags = {item.tag for item in dbbq.get_all(SatelliteModel)}
    satellite_tags = set(SATELLITES.keys())
    res = set(satellite_tags).difference(tmp_satellite_tags)
    if res:
        satellites = []
        for tag in res:
            satellites.append(SatelliteModel(tag=tag, name=SATELLITES[tag]))
        dbbq.bulk_insert_2(satellites)

    satellites_obj = {item.tag: item.id for item in dbbq.get_all(SatelliteModel)}
    return satellites_obj


def create_composite_files(
    dbbq: DefaultDataBaseQuery,
    composite_files: list,
    composite_names: dict,
    satellite_id: int,
    datetime_id: int
):
    logging.info("Perform create composite files")
    composite_model_files = []

    for composite_filename in composite_files:
        item = FileCompositeModel(
            filename=composite_filename["filename"],
            access_tiles=True,
            datetime_created=datetime.now(),
            datetime_id=datetime_id,
            composite_id=composite_names[composite_filename["type"]],
            satellite_id=satellite_id,
        )
        composite_model_files.append(item)

    dbbq.bulk_insert_2(composite_model_files)


def fetch_datetime_satellite(gitco_filename_data: list) -> tuple:
    gitco_filename_data.sort()
    gitco_filename_first = gitco_filename_data[0][-2:]
    datetime_formatted = format_date_time(" ".join(gitco_filename_first), "%Y%m%d %H%M")
    satellite = gitco_filename_data[0][0]
    return datetime_formatted, satellite


def get_or_create_datetime(dbbq: DefaultDataBaseQuery, datetime_formatted) -> DateTimeModel:
    logging.info("Perform get or create datetime")

    datetime_obj = dbbq.get_object_or_none(DateTimeModel, datetime=datetime_formatted)
    if not datetime_obj:
        datetime_obj = dbbq.insert_data(
            DateTimeModel(datetime=datetime_formatted)
        )

    return datetime_obj


def read_fire_values(dbbq: DefaultDataBaseQuery, fire_value_filenames: list, satellite_id: int, datetime_id: int):
    logging.info("Perform read fire values")

    fire_values = []
    for item in fire_value_filenames:
        with open(item['filename'], 'r') as f:
            for line in f.readlines():
                line = line.rstrip('\n')
                latitude, longitude, temperature, *_ = line.split(',')
                fire_value = FireValueModel(
                    longitude=longitude,
                    latitude=latitude,
                    temperature=temperature,
                    resolution=FireValueModel.RESOLUTION_SATELLITE[item["type"]],
                    satellite_id=satellite_id,
                    datetime_id=datetime_id
                )
                fire_values.append(fire_value)

    dbbq.bulk_insert_2(fire_values)


def check_add_data(dbbq: DefaultDataBaseQuery,
                   composite_filenames,
                   fire_value_filenames: list,
                   satellite: str,
                   datetime_formatted) -> bool:
    global confirm_all
    print("-> Composite filenames".upper())
    for item in composite_filenames:
        print(f"{item['filename']}, {item['type']}")

    datetime_obj = dbbq.get_object_or_none(DateTimeModel, datetime=datetime_formatted)
    if datetime_obj:
        print("-----")
        print(f"{datetime_formatted} is exists into DataBase.")

        items = list(dbbq.get_all_by_filter(FileCompositeModel, datetime_id=datetime_obj.id))
        print(f"Count file composite model items: {len(items)}, by datetime: {datetime_formatted}")
        for item in items:
            print(item.filename)

    print("-> Fire value filenames".upper())
    for item in fire_value_filenames:
        print(f"{item['filename']}, {item['type']}")

    while answer := str(input(f"Are you continue? y/n/a/s/d(delete all) \n "
                              f"y - confirm current. \n "
                              f"n dont confirm current. \n "
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
            dbbq.delete_all()
            exit(0)


def copy_file_to_tif_dir(composite_filenames: list, datetime_formatted: datetime, satellite: str):
    date, time = datetime_formatted.strftime("%Y%m%d %H%M").split(' ')
    path = f"{conf.PATH_TO_TIF_DIRS}/{satellite}/{date}/{time}"
    Path(path).mkdir(parents=True, exist_ok=True)
    for item in composite_filenames:
        filename = os.path.basename(item["filename"])
        dst_path = f"{path}/{filename}"
        if not os.path.exists(dst_path):
            shutil.copy(item["filename"], dst_path)


def main():
    dbbq = DefaultDataBaseQuery()

    composite_names = get_and_create_composites(dbbq)
    satellites = get_and_create_satellites(dbbq)

    composite_filenames = []
    fire_value_filenames = []
    gitco_filename_data = []

    with open(conf.PATH_TO_FILE_DIRS, 'r') as f:
        for path in f.readlines():
            path = path.rstrip('\n')

            gitco_filename_data.clear()
            fire_value_filenames.clear()
            composite_filenames.clear()

            for filename in os.listdir(path):
                if match := pattern_composite.search(filename):
                    composite_filenames.append({"filename": f"{path}/{filename}", "type": match.groups()[0]})
                elif match := pattern_v375m_v750m_fire_value.search(filename):
                    type_fv = TYPE_FIRE_VALUE[match.groups()[0]]
                    fire_value_filenames.append({"filename": f"{path}/{filename}", "type": type_fv})
                elif match := pattern_GITCO.search(filename):
                    gitco_filename_data.append(match.groups())

            datetime_formatted, satellite = fetch_datetime_satellite(gitco_filename_data)
            satellite_id = satellites[SATELLITE_TAGS[satellite]]
            #
            if not confirm_all:
                if not check_add_data(dbbq, composite_filenames, fire_value_filenames, satellite, datetime_formatted):
                    continue

            datetime_obj = get_or_create_datetime(dbbq, datetime_formatted)

            read_fire_values(dbbq, fire_value_filenames, satellite_id, datetime_obj.id)

            # copeing
            copy_file_to_tif_dir(composite_filenames, datetime_formatted, SATELLITE_TAGS[satellite])

            create_composite_files(dbbq, composite_filenames, composite_names, satellite_id, datetime_obj.id)


if __name__ == '__main__':
    main()