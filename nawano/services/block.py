# -*- coding: utf-8 -*-

from nanopy.crypto import nano_account, account_nano
from ._base import NawanoService


def calc_balance(v1, v2):
    return str(int(v1) + int(v2))


class BlockService(NawanoService):
    @property
    def receivables(self):
        for address, pending in self.__state__.network_pending:
            if not pending:
                continue

            for _hash, block in pending.items():
                account = self.__state__.client.get_account(address)
                previous = account['frontier'] if account else '0' * 64
                work_hash = previous if account else nano_account(address)

                new_balance = calc_balance(
                    account['balance'], block['amount']
                ) if account else block['amount']

                yield {
                    'representative': self.__state__.representative,
                    'balance': new_balance,
                    'link': _hash,
                    'account': address,
                    'previous': previous,
                }, work_hash

    def get_sendblock(self, seed, account, recipient):
        """account = self.__state__.client.get_account(account)
        recipient = self.__state__.client.get_account(recipient)

        yield {
                  'representative': self.__state__.representative,
                  'balance': new_balance,
                  'link': _hash,
                  'account': address,
                  'previous': previous,
        }, work_hash"""
        pass

    def transaction_summary(self, account_from, alias_to, amount):
        return self._format_output([
            self.get_header('new transaction', color='yellow'),
            'from: {0}/{1}'.format(account_from.name, account_nano(account_from.public_key)),
            'to: {0}/{1}'.format(alias_to.name, alias_to.address),
            'amount: {0}'.format(amount) + '\n'
        ])

    def broadcast(self, block):
        return self.__state__.client.broadcast_block(block)
