# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from nawano.utils import from_raw

from nawano.db import Base, get_db_session
from .wallet import Wallet
from ._base import BaseMixin


class Account(Base, BaseMixin):
    __tablename__ = 'account'

    idx = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    wallet_id = Column(String, ForeignKey('wallet.id'), primary_key=True)
    wallet = relationship(Wallet)

    public_key = Column(String, unique=True)
    available_raw = Column(String, nullable=False, default='0')
    pending_raw = Column(String, nullable=False, default='0')
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now())

    UniqueConstraint(wallet_id, name, name='uc_wallet_account_name')

    @hybrid_property
    def available(self):
        return from_raw(self.available_raw)

    @hybrid_property
    def pending(self):
        return from_raw(self.pending_raw)

    @classmethod
    def get_next_idx(cls, wallet_id):
        with get_db_session() as s:
            curr_idx = s.query(func.max(Account.idx)).filter_by(wallet_id=wallet_id).one()[0]

        return 0 if curr_idx is None else curr_idx + 1

    @classmethod
    def query(cls, **kwargs):
        return cls._query(**kwargs)

    @classmethod
    def update(cls, public_key, **kwargs):
        existing = cls.query(public_key=public_key).one()
        return cls._update(existing, **kwargs)

    @classmethod
    def insert(cls, **kwargs):
        account = Account(**kwargs)
        cls._add(account)
        return kwargs['public_key']
