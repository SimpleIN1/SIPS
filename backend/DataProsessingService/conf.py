import os
from dotenv import load_dotenv

load_dotenv()


POSTGRES_HOST = os.getenv("POSTGRES_HOST", '127.0.0.1')
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5434)
POSTGRES_DB = os.getenv("POSTGRES_DB", "composite_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "test")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")

SQLALCHEMY_DATABASE_URI=(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
                         f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
SQLALCHEMY_ECHO = False

PATH_TO_FILE_DIRS = os.getenv("PATH_TO_FILE_DIRS")
PATH_TO_TIF_DIRS = os.getenv("PATH_TO_TIF_DIRS")
