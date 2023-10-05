from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

from src import config

engine = create_engine(config.DATABASE_URL)

Session = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_session():
    return Session
