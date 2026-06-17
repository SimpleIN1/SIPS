import os
import re
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_COMPOSITE_DATABASE_URI = os.getenv("SQLALCHEMY_COMPOSITE_DATABASE_URI")
SQLALCHEMY_COMPOSITE_DATA_DATABASE_URI = os.getenv("SQLALCHEMY_COMPOSITE_DATA_DATABASE_URI")

SQLALCHEMY_ECHO = False

PATH_TO_FILE_DIRS = os.getenv("PATH_TO_FILE_DIRS")
PATH_TO_TIF_DIRS = os.getenv("PATH_TO_TIF_DIRS")
PATH_TO_CUTTING_FILES = os.getenv("PATH_TO_CUTTING_FILES")
PATH_FILE_OUTDATA = os.getenv("PATH_FILE_OUTDATA")


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

regex = r"viirs_([a-z\d]+)_"
pattern_composite = re.compile(regex)

regex_datetime = r"d(\d{8})_t(\d{4})"
pattern_datetime = re.compile(regex_datetime)

regex_v375m_v750m_fire_value = r"^(VF375|FL).+\.txt$"
pattern_v375m_v750m_fire_value = re.compile(regex_v375m_v750m_fire_value)

regex_GITCO = r"^GITCO_(\w+)_d(\d{8})_t(\d{4}).+\.h5$"
pattern_GITCO = re.compile(regex_GITCO)
