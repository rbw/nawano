# -*- coding: utf-8 -*-

from functools import lru_cache
from datetime import datetime
from nanopy.crypto import account_nano

from nawano.clients import RPC
from nawano.models import ConfigAttribute, Account, State, Wallet
from nawano.exceptions import NoRecordsFound, NoActiveWallet


class StateService(object):
    @property
    def _state(self):
        return State.query().first()

    @lru_cache()
    def get_announced(self, name):
        return getattr(self._state, self._as_announced(name))

    @lru_cache()
    def get_active_wallet(self):
        wallet = State.get_wallet()
        if not wallet:
            raise NoActiveWallet

        return wallet

    @lru_cache()
    def get_wallet_funds(self, wallet_id):
        available, pending = [0, 0]

        for account in Account.query(wallet_id=wallet_id).all():
            available += account.available
            pending += account.pending

        return {
            'available': available,
            'pending': pending
        }

    @property
    def wallet(self):
        return self.get_active_wallet()

    @staticmethod
    def _as_announced(name):
        return '{0}_{1}'.format(name, 'announced')

    def set_announced(self, name):
        State.set(**{name + '_announced': datetime.now().replace(microsecond=0)})
        self.get_announced.cache_clear()

    def set_wallet(self, wallet_id):
        wallet = Wallet.query(id=wallet_id).one_or_none()

        if not wallet:
            raise NoRecordsFound

        State.set(wallet_id=wallet.id)
        self.get_active_wallet.cache_clear()

    @property
    def wallet_funds(self):
        return self.get_wallet_funds(self.wallet.id)

    @property
    def network(self):
        return RPC(ConfigAttribute.get_one('backend').value)

    def get_accounts(self, **kwargs):
        return Account.query(wallet_id=self.wallet.id, **kwargs).all()

    @property
    def pending_blocks(self):
        try:
            accounts = self.get_accounts()
        except NoActiveWallet:
            return []

        addresses = [account_nano(account.public_key) for account in accounts]
        return self.network.get_pending(addresses)
