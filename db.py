# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Database connection details
hostname = "project-db-stu2.smhrd.com"
port = 3307
username = "cgi_3_230524_2"
password = "smhrd2"
database = "cgi_3_230524_2"

# Create the database engine
database_url = f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}"
engine = create_engine(database_url)


session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
Base = declarative_base()
Base.query = session.query_property()

