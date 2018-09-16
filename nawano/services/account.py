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
        for address, pending in self.__state__.pending_blocks:
            account = self.__state__.network.get_account(address)
            available_raw = account['balance'] if account else 0
            pending_raw = 0

            if pending:
                for block in pending.values():
                    pending_raw += int(block['amount'])

            self.__model__.update(
                nano_account(address),
                available_raw=str(available_raw),
                pending_raw=str(pending_raw)
            )

    def get_details(self, **kwargs):
        account = self.get_one(wallet_id=self.__state__.wallet.id, **kwargs)

        if not account:
            raise NawanoError('no such account')

        return self._format_output([
            self.get_header('account'),
            'index: ' + str(account.idx),
            'name: ' + account.name,
            'updated: ' + str(account.updated_on),
            'address: ' + account_nano(account.public_key),
            'public_key: ' + account.public_key.upper(),
            self.get_highlighted('funds') + self.funds_text({
                'available': account.available,
                'pending': account.pending,
            }),
            '\n',
        ])

    @property
    def _table_header(self):
        return ['name', 'index', 'address', 'available', 'pending']

    def _get_table_body(self, accounts):
        for a in accounts:
            yield [
                a.name,
                a.idx,
                '…{0}'.format(account_nano(a.public_key)[-8:]),
                a.available,
                a.pending
            ]

    def get_table(self, **kwargs):
        accounts = self.__state__.get_accounts(**kwargs)

        if not accounts:
            raise NawanoError('no accounts found')

        return self.get_text_table(self._table_header, self._get_table_body(accounts))
