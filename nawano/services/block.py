# -*- coding: utf-8 -*-

from decimal import Decimal

from libn import account_get, account_key

from nawano.utils import to_raw
from ._base import NawanoService


class BlockService(NawanoService):
    @property
    def receivables(self):
        for address, pending in self.__state__.pending_blocks:
            if not pending:
                continue

            for _hash, block in pending.items():
                account = self.__state__.network.get_account(address)
                previous = account['frontier'] if account else '0' * 64
                work_hash = previous if account else account_key(address)

                new_balance = (
                    str(
                        int(account['balance']) + int(block['amount'])
                    ) if account
                    else block['amount']
                )

                yield {
                    'representative': self.__state__.wallet.representative_address,
                    'balance': new_balance,
                    'link': _hash,
                    'account': address,
                    'previous': previous,
                }, work_hash

    def get_sendblock(self, account, alias_to, amount, _):
        address = account_get(account.public_key)
        n_account = self.__state__.network.get_account(address)
        new_balance = str(int(n_account['balance']) - int(to_raw(amount)))

        return {
              'representative': self.__state__.wallet.representative_address,
              'balance': new_balance,
              'link': account_key(alias_to.address),
              'account': address,
              'previous': n_account['frontier']
        }, n_account['frontier']

    def transaction_summary(self, account_from, alias_to, send_amount, available):
        return self._format_output([
            self.get_header('new transaction', color='yellow'),
            'from: {0}/{1}'.format(account_from.name, account_get(account_from.public_key)),
            'to: {0}/{1}'.format(alias_to.name, alias_to.address),
            'amount: {0} ({1} available after send)'.format(
                send_amount,
                Decimal(available) - Decimal(send_amount)
            ) + '\n'
        ])

    def broadcast(self, block):
        return self.__state__.network.broadcast_block(block)
