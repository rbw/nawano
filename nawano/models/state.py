# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from nawano.db import Base
from ._base import BaseMixin
from .wallet import Wallet


class State(Base, BaseMixin):
    __tablename__ = 'state'

    id = Column(Integer, primary_key=True)

    wallet_id = Column(String, ForeignKey('wallet.id'))
    wallet = relationship(Wallet, foreign_keys=wallet_id)

    pending_announced = Column(DateTime, default=BaseMixin.big_bang, nullable=False)
    weight_announced = Column(DateTime, default=BaseMixin.big_bang, nullable=False)

    @classmethod
    def install(cls):
        return cls._add(State(id=1))

    @classmethod
    def get_wallet(cls):
        return cls.query().first().wallet

    @classmethod
    def set(cls, **kwargs):
        return cls._update(cls.query().first(), **kwargs)
