from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = "mysql+pymysql://root:812004@localhost:3306/todoapp"


engine = create_engine(DB_URL)

session_local = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()