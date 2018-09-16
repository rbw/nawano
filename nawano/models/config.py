# -*- coding: utf-8 -*-

from sqlalchemy import String, Column

from nawano.db import Base
from ._base import BaseMixin


class ConfigAttribute(Base, BaseMixin):
    __tablename__ = 'config'

    name = Column(String, primary_key=True, nullable=False)
    value = Column(String, nullable=False)
    description = Column(String)
    type = Column(String)

    @classmethod
    def query(cls, **kwargs):
        return cls._query(**kwargs)

    @classmethod
    def update(cls, name, **kwargs):
        existing = cls.query(name=name).one()
        return cls._update(existing, value=kwargs['value'])

    @classmethod
    def insert(cls, **kwargs):
        attr = ConfigAttribute(**kwargs)
        return cls._add(attr)

    @classmethod
    def get_one(cls, name):
        attr = cls.query(name=name).one_or_none()
        if not attr:
            return None

        attr.value = eval(attr.type)(attr.value)
        return attr
