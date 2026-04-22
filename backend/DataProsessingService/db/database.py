from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import conf

engine = create_engine(
    conf.SQLALCHEMY_DATABASE_URI,
    echo=conf.SQLALCHEMY_ECHO
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
