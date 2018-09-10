# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from nawano.db import Base
from ._base import BaseMixin
from .wallet import Wallet


class State(Base, BaseMixin):
    __tablename__ = 'state'

    id = Column(Integer, primary_key=True)
    wallet_id = Column(String, ForeignKey('wallet.id'))
    wallet = relationship(Wallet, foreign_keys=wallet_id)
    backend = Column(String, default='https://getcanoe.io/rpc')
    is_syncing = Column(Boolean, default=False, nullable=False)
    last_synced_on = Column(DateTime, default=BaseMixin.big_bang, nullable=False)
    pending_announced_on = Column(DateTime, default=BaseMixin.big_bang, nullable=False)

    @classmethod
    def install(cls):
        return cls._add(State(id=1))

    @classmethod
    def get_wallet(cls):
        # return cls.query(State.wallet)
        return cls.query().first().wallet

    @classmethod
    def set(cls, **kwargs):
        return cls._update(cls.query().first(), **kwargs)
