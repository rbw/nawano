# -*- coding: utf-8 -*-

from datetime import datetime
from nanopy.crypto import nano_account, account_nano, seed_keys

from nawano.models import Account
from nawano.exceptions import NawanoError, NoActiveWallet
from nawano.utils import decrypt, stylize, bin2ascii


from ._base import NawanoService


class AccountService(NawanoService):
    __model__ = Account

    def insert(self, **kwargs):
        wallet = self.__state__.wallet
        account_name = kwargs.pop('name')

        # Decrypt seed
        seed = decrypt(wallet.seed, kwargs.pop('password'))

        # Get next ID from input or DB
        account_idx = kwargs.pop('idx', None) or self.__model__.get_next_idx(wallet.id)

        # Derive account from seed
        sk, pk = seed_keys(seed.decode('ascii'), int(account_idx))

        account_pk = self.__model__.insert(
            idx=account_idx,
            name=account_name,
            public_key=bin2ascii(pk),
            wallet_id=wallet.id,
            **kwargs
        )

        return account_pk

    def refresh_balances(self):
        try:
            self.__state__.syncing = True
        except NoActiveWallet:
            return

        for address, pending in self.__state__.pending_blocks:
            account = self.__state__.network.get_account(address)
            balance_raw = account['balance'] if account else 0
            pending_raw = 0

            if pending:
                for block in pending.values():
                    pending_raw += int(block['amount'])

            self.update_funds(
                nano_account(address),
                balance_raw=str(balance_raw),
                pending_raw=str(pending_raw)
            )

        self.__state__.syncing = False

    def update_funds(self, public_key, **kwargs):
        self.__model__.update(public_key, **kwargs)
        self.__state__.synced_on = datetime.now().replace(microsecond=0)

    def get_details(self, **kwargs):
        if not self.__state__:
            raise NoActiveWallet

        account = self.get_one(wallet_id=self.__state__.wallet.id, **kwargs)

        if not account:
            raise NawanoError('no such account')

        return self._format_output([
            self.get_header('account'),
            'name: {0}'.format(account.name),
            'address: {0}'.format(account_nano(account.public_key)),
            'public_key: {0}'.format(account.public_key.upper()),
            'index: {0}'.format(account.idx),
            'created_on: {0}'.format(account.created_on),
            'balance: {0} ({1})'.format(
                account.balance,
                '{0} pending'.format(self.get_count_styled(account.pending))
            ) + '\n\n'
        ])

    @property
    def _table_header(self):
        return ['name', 'index', 'address', 'balance', 'pending']

    def _get_table_body(self, accounts):
        for a in accounts:
            yield [
                a.name,
                a.idx,
                '…{0}'.format(account_nano(a.public_key)[-8:]),
                a.balance,
                a.pending
            ]

    def get_table(self, **kwargs):
        accounts = self.__state__.accounts(**kwargs)

        if not accounts:
            raise NawanoError('no accounts found')

        return self.get_text_table(self._table_header, self._get_table_body(accounts))
