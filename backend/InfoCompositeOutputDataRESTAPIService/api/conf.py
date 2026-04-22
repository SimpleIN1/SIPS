import os
from dotenv import load_dotenv, find_dotenv

load_dotenv()

DEBUG = (bool(int(os.getenv("DEBUG", 1))))

POSTGRES_HOST = os.getenv("POSTGRES_HOST", '127.0.0.1')
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5434)
POSTGRES_DB = os.getenv("POSTGRES_DB", "composite_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "test")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")

SQLALCHEMY_DATABASE_URI = (f"postgresql://{POSTGRES_USER}:"
                           f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
SQLALCHEMY_ECHO = False

# regular expression for only symbols a-z, A-Z, 0-9 limited to 20 symbols
REGEX_PARAMS_SATELLITE = r"^[a-zA-Z0-9]{0,20}$"

CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 250))
CACHE_TYPE = os.getenv("CACHE_TYPE", 'RedisCache')
CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL", "redis://localhost:6379/0")

MAIN_ROUTE = "/api/vicod"
API_SPEC_URL = f"{MAIN_ROUTE}/docs/swagger"
