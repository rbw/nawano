# -*- coding: utf-8 -*-

from contextlib import contextmanager

from sqlalchemy import create_engine, MetaData
from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from nawano.settings import SQLALCHEMY_DATABASE_URI


engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    poolclass=SingletonThreadPool,
    connect_args={'check_same_thread': False}
)

Session = scoped_session(
    sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False
    )
)


def filter_empty(data):
    return dict(filter(lambda x: x[1], data.items()))


@contextmanager
def get_db_session():
    try:
        yield Session
    finally:
        Session.remove()


Base = declarative_base()
metadata = MetaData()
