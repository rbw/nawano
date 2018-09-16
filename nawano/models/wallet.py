# -*- coding: utf-8 -*-

from functools import lru_cache
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from nawano.db import Base

from .account import Account
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
    representative = relationship(Representative, lazy=False)

    ForeignKeyConstraint(
        (representative_address, representative_alias),
        (Representative.address, Representative.alias)
    ),

    @classmethod
    def update(cls, wallet_id, **kwargs):
        wallet = cls.query(id=wallet_id).one()
        return cls._update(wallet, **kwargs)

    @classmethod
    def insert(cls, **kwargs):
        kwargs['id'] = str(uuid4())
        cls._add(Wallet(**kwargs))
        return kwargs['id']

    @classmethod
    @lru_cache()
    def get_funds(cls, wallet_id):
        available, pending = [[a.available, a.pending] for a in Account.query(wallet_id=wallet_id).all()]

        return {
            'available': sum(available),
            'pending': sum(pending)
        }
