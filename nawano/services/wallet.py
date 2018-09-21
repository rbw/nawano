# -*- coding: utf-8 -*-

from nawano.models import Wallet, Account, Representative
from nawano.utils import encrypt, generate_seed, stylize

from ._base import NawanoService


class WalletService(NawanoService):
    __model__ = Wallet

    def insert(self, **kwargs):
        wallet_name = kwargs.pop('name')
        seed = kwargs.pop('seed', generate_seed())

        return self.__model__.insert(name=wallet_name, seed=encrypt(seed, kwargs.pop('password')))

    @property
    def _table_header(self):
        return ['name', 'accounts', 'available', 'pending']

    def _get_table_body(self, wallets):
        for wallet in wallets:
            accounts = Account.query(wallet_id=wallet.id).all()
            funds = self.__state__.get_wallet_funds(wallet.id)
            yield [
                wallet.name,
                len(accounts),
                funds['available'],
                funds['pending']
            ]

    def get_table(self, **kwargs):
        wallets = self.get_many(raise_on_empty=True, **kwargs)
        return self.get_text_table(self._table_header, self._get_table_body(wallets))

    @staticmethod
    def _format_rep_details(rep):
        return (
            '\n{0}name: {1}\n{0}address: {2}\n{0}weight: {3}\n{0}uptime: {4:0.2f}%\n'
            .format(' '*2, rep.alias, rep.address, rep.weight, float(rep.uptime))
        )

    def get_details(self, **kwargs):
        wallet = self.get_one(**kwargs, raise_on_empty=True)
        funds = self.__state__.get_wallet_funds(wallet.id)
        accounts = Account.query(wallet_id=wallet.id).all()

        if not wallet.representative_address:
            rep_text = stylize('\n  not set\n', color='red')
        elif isinstance(wallet.representative, Representative):
            rep_text = self._format_rep_details(wallet.representative)
        else:
            rep_text = '\n  address: {0}\n'.format(wallet.representative_address)

        return self._format_output([
            self.get_header('wallet'),
            'name: ' + wallet.name,
            'updated: ' + str(wallet.updated_on),
            'accounts: {0}'.format(len(accounts)),
            self.get_highlighted('funds') + self.funds_text(funds),
            self.get_highlighted('representative') + rep_text + '\n',
        ])
