# -*- coding: utf-8 -*-

import json
import requests

from simplejson.scanner import JSONDecodeError
from nawano.exceptions import UnexpectedBackendResponse


class RPC(object):
    def __init__(self, uri):
        self._uri = uri
        self._session = requests.session()

    def _request(self, payload):
        try:
            response = self._session.post(url=self._uri, json=payload).json()
        except JSONDecodeError:
            raise UnexpectedBackendResponse(message='unexpected response from server')

        if 'error' in response:
            raise UnexpectedBackendResponse(message=response['error'])

        return response

    def _get_blocks(self, payload):
        response = self._request(payload)
        return response['blocks'] if 'blocks' in response else {}

    def validate_address(self, address):
        response = self._request({'action': 'validate_account_number', 'account': address})
        return response['valid'] == '1'

    def broadcast_block(self, block):
        block['type'] = 'state'
        return self._request({'action': 'process', 'block': json.dumps(block)})

    def get_pending(self, addresses):
        try:
            blocks = self._get_blocks({'action': 'accounts_pending', 'source': 'true', 'accounts': addresses})
            return blocks.items() if blocks else {}
        except UnexpectedBackendResponse as err:
            if not err.message == 'Account not found':
                raise

            return {}

    def get_supply(self):
        return self._request({'action': 'available_supply'})

    def get_representatives(self):
        return self._request({'action': 'representatives'})

    def get_account(self, address):
        payload = {
            'action': 'account_info',
            'account': address,
            'representative': 'true',
            'weight': 'true',
        }

        try:
            return self._request(payload)
        except UnexpectedBackendResponse as err:
            if not err.message == 'Account not found':
                raise

            return None

    def get_blocks_info(self, hashes):
        return self._get_blocks({'action': 'blocks_info', 'hashes': hashes})

    def get_balances(self, addresses):
        try:
            return self._request({'action': 'accounts_balances', 'accounts': addresses}).get('balances')
        except UnexpectedBackendResponse as err:
            if not err.message == 'Account not found':
                raise

            return None
