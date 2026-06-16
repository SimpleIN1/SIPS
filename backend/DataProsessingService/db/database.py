from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import conf


class PostgreSQLBase:

    def __init__(self, database_uri, sqlalchemy_echo):
        self.engine = create_engine(
            database_uri,
            echo=sqlalchemy_echo
        )

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

        self.Base = declarative_base()


composite_pbase = PostgreSQLBase(conf.SQLALCHEMY_COMPOSITE_DATABASE_URI,
                                 conf.SQLALCHEMY_ECHO)
composite_data_pbase = PostgreSQLBase(conf.SQLALCHEMY_COMPOSITE_DATA_DATABASE_URI,
                                      conf.SQLALCHEMY_ECHO)
