# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.sql import func

from nawano.db import Base
from ._base import BaseMixin


class Representative(Base, BaseMixin):
    __tablename__ = 'representative'

    alias = Column(String, primary_key=True)
    address = Column(String, primary_key=True)
    uptime = Column(String, nullable=False)
    delegators = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    @classmethod
    def query(cls, **kwargs):
        return cls._query(**kwargs)
