# -*- coding: utf-8 -*-

from nawano.models import Wallet, Account, Representative
from nawano.exceptions import NawanoError, NoSuchWallet
from nawano.utils import encrypt, generate_seed, stylize

from ._base import NawanoService


class WalletService(NawanoService):
    __model__ = Wallet

    def insert(self, **kwargs):
        wallet_name = kwargs.pop('name')
        seed = generate_seed()

        return self.__model__.insert(name=wallet_name, seed=encrypt(seed, kwargs.pop('password')))

    @property
    def _table_header(self):
        return ['name', 'accounts', 'balance', 'pending']

    def _get_table_body(self, wallets):
        for w in wallets:
            accounts = Account.query(wallet_id=w.id).all()
            funds = self.__model__.get_funds(w.id)
            yield [
                w.name,
                len(accounts),
                funds['balance'],
                funds['pending']
            ]

    def get_table(self, **kwargs):
        wallets = self.get_many(**kwargs)
        if not wallets:
            raise NawanoError('no wallets found')

        return self.get_text_table(self._table_header, self._get_table_body(wallets))

    def _format_rep_details(self, rep):
        return (
            '\n name: {0}\n address: {1}\n weight: {2}\n uptime: {3:0.2f}%\n'
            .format(rep.alias, rep.address, rep.weight, float(rep.uptime))
        )

    def get_details(self, **kwargs):
        wallet = self.__model__.query(**kwargs).one_or_none()
        if not wallet:
            raise NoSuchWallet

        funds = self.__model__.get_funds(wallet.id)
        accounts = Account.query(wallet_id=wallet.id).all()

        if not wallet.representative_address:
            rep_text = stylize('none configured', color='red')
        elif isinstance(wallet.representative, Representative):
            rep_text = self._format_rep_details(wallet.representative)
        else:
            rep_text = '\n address: {0}\n'.format(wallet.representative_address)

        return self._format_output([
            self.get_header('wallet'),
            'name: {0}'.format(wallet.name),
            'created_on: {0}'.format(wallet.created_on),
            'synced_on: {0}'.format(self.__state__.synced_on),
            'accounts: {0}'.format(len(accounts)),
            'representative: {0}'.format(rep_text),
            'funds: \n balance: {0} \n pending: {1}\n\n'.format(funds['balance'], funds['pending']),
        ])
