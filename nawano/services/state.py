# -*- coding: utf-8 -*-

from nanopy.crypto import account_nano

from nawano.clients import RPC
from nawano.models import ConfigAttribute, Account, State, Wallet
from nawano.exceptions import NoSuchWallet, NoActiveWallet, SyncAlreadyRunning


class StateService(object):
    @property
    def _state(self):
        return State.query().first()

    @property
    def wallet(self):
        wallet = State.get_wallet()
        if not wallet:
            raise NoActiveWallet

        return wallet

    @property
    def wallet_funds(self):
        return self.wallet.get_funds(self.wallet.id)

    @property
    def network(self):
        return RPC(ConfigAttribute.get_one('backend').value)

    def set_wallet(self, wallet_id):
        wallet = Wallet.query(id=wallet_id).one_or_none()

        if not wallet:
            raise NoSuchWallet

        State.set(wallet_id=wallet.id)

    @property
    def funds(self):
        return self.wallet.get_funds(self.wallet.id)

    def get_accounts(self, **kwargs):
        return Account.query(wallet_id=self.wallet.id, **kwargs).all()

    @property
    def syncing(self):
        return State.is_syncing

    @syncing.setter
    def syncing(self, new_state):
        if new_state is True and self.syncing is True:
            raise SyncAlreadyRunning

        State.set(is_syncing=new_state)

    @property
    def synced_on(self):
        return self._state.last_synced_on

    @synced_on.setter
    def synced_on(self, value):
        State.set(last_synced_on=value)

    @property
    def pending_announced(self):
        return self._state.pending_announced_on

    @pending_announced.setter
    def pending_announced(self, value):
        State.set(pending_announced_on=value)

    @property
    def pending_blocks(self):
        try:
            accounts = self.get_accounts()
        except NoActiveWallet:
            return []

        addresses = [account_nano(account.public_key) for account in accounts]
        return self.network.get_pending(addresses)
