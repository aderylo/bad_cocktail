import os

from sqlalchemy import create_engine
from sqlmodel import SQLModel
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PWD = os.getenv("POSTGRES_PWD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = "bd"

db_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}/{DB_NAME}"
db_url = f"postgresql://scott:tiger@lkdb/bd"

engine = create_engine(db_url)
Session = scoped_session(sessionmaker(bind=engine))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def clean_up_db():
    SQLModel.metadata.drop_all(engine)
