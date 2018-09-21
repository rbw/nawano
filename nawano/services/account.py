# -*- coding: utf-8 -*-

from libn import account_key, account_get, deterministic_key

from nawano.models import Account
from nawano.exceptions import NawanoError
from nawano.utils import decrypt


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
        sk, pk, _ = deterministic_key(seed.decode('ascii'), int(account_idx))

        # Look for existing account with this PK
        existing = self.__model__.query(public_key=pk).one_or_none()

        if existing:
            raise NawanoError('account key conflicts with {0} in wallet {1}'.format(existing.name, existing.wallet.name))

        account_pk = self.__model__.insert(
            idx=account_idx,
            name=account_name,
            public_key=pk,
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
                account_key(address),
                available_raw=str(available_raw),
                pending_raw=str(pending_raw)
            )

        self.__state__.get_wallet_funds.cache_clear()

    def get_details(self, **kwargs):
        account = self.get_one(wallet_id=self.__state__.wallet.id, raise_on_empty=True, **kwargs)

        return self._format_output([
            self.get_header('account'),
            'index: ' + str(account.idx),
            'name: ' + account.name,
            'updated: ' + str(account.updated_on),
            'address: ' + account_get(account.public_key),
            'pubkey: ' + account.public_key.upper(),
            self.get_highlighted('funds') + self.funds_text({
                'available': account.available,
                'pending': account.pending,
            }),
            '\n',
        ])

    @property
    def _table_header(self):
        return ['name', 'index', 'address', 'available', 'pending']

    @staticmethod
    def _get_table_body(accounts):
        for a in accounts:
            yield [
                a.name,
                a.idx,
                '…{0}'.format(account_get(a.public_key)[-8:]),
                a.available,
                a.pending
            ]

    def get_table(self, **kwargs):
        accounts = self.__state__.get_accounts(**kwargs)

        if not accounts:
            raise NawanoError('no accounts found')

        return self.get_text_table(self._table_header, self._get_table_body(accounts))
