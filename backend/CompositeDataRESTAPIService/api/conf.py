import os
from dotenv import load_dotenv, find_dotenv

load_dotenv()

# conf app
DEBUG = (bool(int(os.getenv("DEBUG", 1))))

COUNT_FILE_DOWNLOAD = int(os.getenv("COUNT_FILE_DOWNLOAD", 30))
EXPANSIONS_ARCHIVE = ["zip", "tar", "rar", "7z"]
# regular expression for only symbols a-z, A-Z, 0-9 limited to 20 symbols
REGEX_PARAMS_SATELLITE = r"^[a-zA-Z0-9]{0,20}$"
REGEX_PARAMS_URL = r"^[a-zA-Z0-9]{0,10}$"

SCHEMA = os.getenv("SCHEMA")
DOMAIN = os.getenv("DOMAIN")
PORT = int(os.getenv("PORT"))
NAME = os.getenv("NAME")

MAIN_ROUTE = "api/vcd"
API_SPEC_URL = f"/{MAIN_ROUTE}/docs/swagger"

PATH_SAFE_CUTTING_IMAGE = "files/images"

DAYS_STORED = 20
TEST_USER = False
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")

COUNT_DOWNLOAD_DAYS = 20
COUNT_DOWNLOAD_LINK_DAYS = 20
COUNT_TASK_CUT_DAYS = 100


ROUTES = {
    "download_by_url": f"/{MAIN_ROUTE}/composites/download/%s"
}

# swagger
SWAGGER_URL = f"/{MAIN_ROUTE}/docs/swagger"  # URL for exposing Swagger UI (without trailing '/')
API_URL = f"{API_SPEC_URL}.json"  # Our API url (can of course be a local resource)


URL_FILE_DOWNLOAD = f"{SCHEMA}://{DOMAIN}{PORT}/{MAIN_ROUTE}/composites/download"


# task celery conf
CLEAR_FILE_DOWNLOAD_TIME = "00:00"
CLEAR_FILE_DOWNLOAD_TIME_SCHEDULE = 10 * 60 * 4


# conf database
POSTGRES_HOST = os.getenv("POSTGRES_HOST", '127.0.0.1')
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5434)
POSTGRES_DB = os.getenv("POSTGRES_DB", "composite_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "test")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")

SQLALCHEMY_DATABASE_URI = (f"postgresql://{POSTGRES_USER}:"
                           f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
SQLALCHEMY_ECHO = False


# conf caching
CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 250))
CACHE_TYPE = os.getenv("CACHE_TYPE", 'RedisCache')
CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL", "redis://localhost:6379/0")


# conf JSONWebToken
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_IDENTITY_CLAIM = "exp"


# celery settings
broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
task_ignore_result = True
broker_connection_retry_on_startup = True

imports = (
    'api.celery.tasks',
)

TIMES_SCHEDULE = {
    'TIME_REMOVE_EXPIRED_URLS': 10.0 * 6 * 10,
}

# email settings
MAIL_SERVER = os.getenv("EMAIL_HOST")
MAIL_PORT = int(os.getenv("EMAIL_PORT"))
MAIL_USE_TLS = (bool(int(os.getenv('EMAIL_USE_TLS', 1))))
MAIL_USERNAME = os.getenv("EMAIL_HOST_USER")
MAIL_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
MAIL_DEBUG = False
