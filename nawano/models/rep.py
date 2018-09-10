# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func

from nawano.db import Base
from ._base import BaseMixin


class Representative(Base, BaseMixin):
    __tablename__ = 'representative'

    address = Column(String, primary_key=True)
    alias = Column(String, nullable=False)
    uptime = Column(String, nullable=False)
    delegators = Column(Integer, nullable=False)
    weight = Column(String, nullable=False)
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
