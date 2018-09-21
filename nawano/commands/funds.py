# -*- coding: utf-8 -*-

import click

from decimal import Decimal
from sys import stdout
from libn import work_generate, account_get, account_key, deterministic_key, sign_block
from nawano.services import block_service, account_service, alias_service, state_service
from nawano.status import with_status
from nawano.utils import password_input, decrypt, from_raw
from nawano.exceptions import NawanoError
from .root import root_group


@with_status(text='generating proof-of-work')
def _pow_generate(_hash):
    return work_generate(_hash)


@with_status(text='refreshing balances')
def _refresh_balances():
    account_service.refresh_balances()
    return None, None


@with_status(text='preparing send-block')
def _sendblock_prepare(**kwargs):
    validated = _validate_send(kwargs)
    block, work_hash = block_service.get_sendblock(*validated)
    return (validated, block, work_hash), None


def _validate_send(payload):
    account_from = account_service.get_one(name=payload['account_from'], wallet_id=state_service.wallet.id)
    n_account = state_service.network.get_account(account_get(account_from.public_key))
    recipient_alias = alias_service.get_one(name=payload['recipient_alias'])
    send_amount = Decimal(payload['amount'])

    if not account_from:
        raise NawanoError('option --account_from must be a valid account name')
    elif not recipient_alias:
        raise NawanoError('option --recipient_alias must be a valid alias')
    elif send_amount <= 0:
        raise NawanoError('amount must be greater than 0')
    elif Decimal(from_raw(n_account['balance'])) < Decimal(send_amount):
        missing = Decimal(send_amount) - Decimal(account_from.available)
        raise NawanoError('insufficient funds (available: {0}, send_amount: {1} (missing: {2}))'
                          .format(account_from.available, send_amount, missing))

    return account_from, recipient_alias, send_amount


@with_status(text='signing transaction')
def _block_sign(block, seed):
    account = account_service.get_one(public_key=account_key(block['account']))
    assert account

    sk, pk, _ = deterministic_key(seed, account.idx)
    return sign_block(sk, pk, block)


@with_status(text='validating')
def _block_validate(block, schema):
    return schema.load(block).data


@with_status(text='broadcasting block')
def _block_broadcast(block):
    return block_service.broadcast(block)


@with_status(text='refreshing balances')
def _refresh_balances():
    return account_service.refresh_balances()


@root_group.group('funds', short_help='send or receive funds')
def funds_group():
    if not state_service.get_accounts():
        raise NawanoError('this operation requires an account')
    elif not state_service.wallet.representative_address:
        raise NawanoError('this operation requires a wallet representative')


@funds_group.command('refresh', short_help='refresh balances now')
def wallet_list():
    _refresh_balances()


@funds_group.command('send', short_help='send funds')
@click.option('--account_from', help='name of account to send from', required=True)
@click.option('--recipient_alias', help='name of recipient address alias', required=True)
@click.option('--amount', help='amount to send', required=True)
def funds_send(**kwargs):
    (validated, block, work_hash), _ = _sendblock_prepare(**kwargs)
    stdout.write(block_service.transaction_summary(*validated, block['balance']))

    stdout.write('\n---\nenter password to proceed or <ctrl+d> to cancel\n')
    password = password_input(validate_confirm=False)
    seed = decrypt(state_service.wallet.seed, password).decode('ascii')

    stdout.write('\nprocessing {0}\n'.format(block['link']))

    # Create PoW based on previous or PK
    block['work'] = _pow_generate(work_hash)

    # Sign block
    block['signature'] = _block_sign(block, seed)

    # Broadcast transaction
    _block_broadcast(block)

    # Refresh balances
    _refresh_balances()


@funds_group.command('pull', short_help='receive pending funds')
def funds_pull():
    p_tot = state_service.wallet_funds['pending']

    if float(p_tot) <= 0:
        raise NawanoError('no pending blocks')

    stdout.write(account_service.get_header('receive'))
    stdout.write('\npending: {0} ~ use <ctrl+d> to cancel\n'.format(p_tot))

    password = password_input(validate_confirm=False)
    seed = decrypt(state_service.wallet.seed, password).decode('ascii')

    for block, work_hash in block_service.receivables:
        stdout.write('\nprocessing {0}\n'.format(block['link']))

        # Create PoW based on frontier
        block['work'] = _pow_generate(work_hash)

        # Sign block
        block['signature'] = _block_sign(block, seed)

        # Broadcast transaction
        _block_broadcast(block)

        # Refresh balances
        _refresh_balances()
