# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

from nawano.db import Base
from ._base import BaseMixin


class Alias(Base, BaseMixin):
    __tablename__ = 'alias'

    address = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now())

    @classmethod
    def query(cls, **kwargs):
        return cls._query(**kwargs)

    @classmethod
    def update(cls, public_key, **kwargs):
        existing = cls.query(public_key=public_key).one()
        return cls._update(existing, **kwargs)

    @classmethod
    def insert(cls, **kwargs):
        account = Alias(**kwargs)
        cls._add(account)
        return kwargs['address']
