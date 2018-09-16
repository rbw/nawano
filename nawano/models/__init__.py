# -*- coding: utf-8 -*-

from nawano.db import Base, engine

from .account import Account
from .wallet import Wallet
from .config import ConfigAttribute
from .alias import Alias
from .rep import Representative
from .state import State


def meta_create_all():
    Base.metadata.create_all(engine)
