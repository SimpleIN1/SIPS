from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from api import conf


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

engine = create_engine(
    conf.SQLALCHEMY_DATABASE_URI,
    echo=conf.SQLALCHEMY_ECHO
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
