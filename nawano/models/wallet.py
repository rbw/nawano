# -*- coding: utf-8 -*-

from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from nawano.db import Base

from .rep import Representative
from ._base import BaseMixin


class Wallet(Base, BaseMixin):
    __tablename__ = 'wallet'

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    seed = Column(String, nullable=False)
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now())

    representative_address = Column(String)
    representative_alias = Column(String)
    representative = relationship(Representative)

    ForeignKeyConstraint(
        (representative_address, representative_alias),
        (Representative.address, Representative.alias)
    ),

    @classmethod
    def query(cls, **kwargs):
        return cls._query(**kwargs)

    @classmethod
    def update(cls, wallet_id, **kwargs):
        wallet = cls.query(id=wallet_id).one()
        res = cls._update(wallet, **kwargs)
        return res

    @classmethod
    def insert(cls, **kwargs):
        kwargs['id'] = str(uuid4())
        cls._add(Wallet(**kwargs))
        return kwargs['id']
