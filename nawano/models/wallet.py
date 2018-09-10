# -*- coding: utf-8 -*-

import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey
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
    created_on = Column(DateTime, default=func.now(), nullable=False)

    rep_addr = Column(String, ForeignKey('representative.address'))
    representative = relationship(Representative, foreign_keys=rep_addr)

    @classmethod
    def update(cls, wallet_id, **kwargs):
        wallet = cls.query(id=wallet_id).one()
        return cls._update(wallet, **kwargs)

    @classmethod
    def insert(cls, **kwargs):
        kwargs['id'] = str(uuid.uuid4())
        cls._add(Wallet(**kwargs))
        return kwargs['id']

    @classmethod
    def get_funds(cls, wallet_id):
        accounts = Account.query(wallet_id=wallet_id).all()
        return {
            'balance': sum([a.balance for a in accounts]),
            'pending': sum([a.pending for a in accounts])
        }

