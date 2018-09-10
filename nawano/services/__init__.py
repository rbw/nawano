# -*- coding: utf-8 -*-

from .wallet import WalletService
from .block import BlockService
from .account import AccountService
from .config import ConfigService
from .alias import AliasService
from .rep import RepresentativeService
from .state import StateService

wallet_service = WalletService()
block_service = BlockService()
account_service = AccountService()
config_service = ConfigService()
alias_service = AliasService()
rep_service = RepresentativeService()
state_service = StateService()
