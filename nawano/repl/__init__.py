# -*- coding: utf-8 -*-

from sys import stdout
from datetime import datetime
from nawano.exceptions import NoActiveWallet
from nawano.services import config_service, state_service
from nawano.utils import stylize


def get_cfg(key):
    return config_service.get(key).value


def get_styled_prompt():
    return [
        ('class:prompt-name', 'nawano'),
        ('class:prompt-marker', u'> '),
    ]


def cooldown_reached(key):
    cooldown_secs = config_service.get('notify_cooldown').value
    return cooldown_secs < (datetime.now() - state_service.get_announced(key)).seconds


def pending_announce():
    try:
        funds = state_service.wallet_funds
    except NoActiveWallet:
        return

    if float(funds['pending']) > 0:
        stdout.write('[{0}] there are pending funds, enter {1} to claim now.\n'.format(
            stylize('info', color='yellow'),
            stylize('funds pull', color='green')
        ))

        state_service.set_announced('pending')


def weight_announce():
    try:
        representative = state_service.wallet.representative
        if not representative or not representative.weight:
            return
    except NoActiveWallet:
        return

    max_weight = config_service.get('max_weight').value

    if representative.weight > max_weight:
        stdout.write('[{0}] your representative has too much weight, type {1} to change\n'.format(
            stylize('info', color='yellow'),
            stylize('wallet representative', color='green')
        ))

        state_service.set_announced('weight')


def get_bottom_toolbar():
    try:
        wallet = state_service.wallet
    except NoActiveWallet:
        return None

    pending_class = (
        'class:bottom-toolbar-pending'
        if
        float(state_service.wallet_funds['pending']) > 0
        else
        'class:bottom-toolbar-value'
    )

    funds = state_service.wallet_funds

    return [
        ('class:bottom-toolbar-logo', ' Ϟ '),
        ('class:bottom-toolbar-key', 'wallet:'),
        ('class:bottom-toolbar-value', str(wallet.name)),
        ('class:bottom-toolbar-key', ' · available:'),
        ('class:bottom-toolbar-value', funds['available']),
        ('class:bottom-toolbar-key', ' · pending:'),
        (pending_class, funds['pending']),
    ]
