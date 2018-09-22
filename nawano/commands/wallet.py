# -*- coding: utf-8 -*-

import click
from prompt_toolkit import prompt
from sys import stdout
from libn import deterministic_key

from nawano.services import wallet_service, state_service, rep_service, account_service
from nawano.utils import password_input, decrypt, stylize
from nawano.status import with_status
from nawano.exceptions import NawanoError
from .root import root_group


@with_status(text='setting active wallet')
def _wallet_set_active(wallet_id):
    state_service.set_wallet(wallet_id)
    account_service.refresh_balances()
    return None, None


@with_status(text='decrypting seed')
def _dump_seed(seed_encrypted, password):
    seed = decrypt(seed_encrypted, password).decode('ascii')
    msg = seed
    return None, msg


@with_status(text='validating seed')
def _validate_seed(seed):
    if len(seed) != 64:
        raise NawanoError('must be exactly 64 chars in size')

    try:
        deterministic_key(seed, 0)
    except ValueError:
        raise NawanoError('must be a hexadecimal string')

    return seed.upper().encode('ascii'), None


@with_status(text='setting representative')
def _wallet_set_representative(address):
    if not state_service.network.validate_address(address):
        raise NawanoError('invalid address format')

    wallet_id = state_service.wallet.id
    wr = {
        'representative_address': address
    }

    rep = rep_service.get_one(address=address)

    wr['representative_alias'] = rep.alias if rep else None
    wallet_service.update(wallet_id, **wr)

    return None, None


@with_status(text='creating wallet')
def _wallet_create(**kwargs):
    wallet_id = wallet_service.insert(**kwargs)
    msg = 'local ID: {0}'.format(wallet_id)
    return wallet_id, msg


def _validate_wallet_name(ctx, param, value):
    if wallet_service.get_one(name=value):
        raise NawanoError('a wallet with that name already exists')

    return wallet_service.validate_name(value)


def _validate_rep_alias(ctx, param, value):
    if not rep_service.get_one(alias=value):
        raise NawanoError('invalid representative alias provided')

    return value


def _validate_rep_address(ctx, param, value):
    if not state_service.network.validate_address(value):
        raise NawanoError('invalid address format')

    return value


@root_group.group('wallet', short_help='wallet operations')
def wallet_group():
    pass


@wallet_group.command('create', short_help='create a new wallet')
@click.option('--name', 'name', help='wallet name', callback=_validate_wallet_name, required=True)
def wallet_create(**kwargs):
    kwargs['password'] = password_input(validate_confirm=True)
    stdout.write('\n')
    wallet_id, _ = _wallet_create(**kwargs)

    if prompt('switch to this wallet? [Y/n] ').lower() in ['', 'y']:
        _wallet_set_active(wallet_id)


@wallet_group.command('import', short_help='create wallet from existing seed')
@click.option('--name', 'name', help='wallet name', callback=_validate_wallet_name, required=True)
def wallet_import(**kwargs):
    seed = password_input(validate_confirm=False, pw1_text='seed: ')
    kwargs['seed'], _ = _validate_seed(seed.decode('ascii'))

    kwargs['password'] = password_input(validate_confirm=True)
    stdout.write('\n')
    wallet_id, _ = _wallet_create(**kwargs)

    if prompt('switch to this wallet? [Y/n] ').lower() in ['', 'y']:
        _wallet_set_active(wallet_id)


@wallet_group.command('use', short_help='set active wallet')
@click.argument('name', required=True)
def wallet_set_active(name):
    wallet = wallet_service.get_one(raise_on_empty=True, name=name)
    _wallet_set_active(wallet.id)


@wallet_group.command('show', short_help='show wallet details')
@click.argument('name', required=True)
def wallet_show(**kwargs):
    stdout.write(wallet_service.get_details(**kwargs))


@wallet_group.command('representative', short_help='set representative')
@click.argument('address', required=True)
def wallet_set_representative(address):
    return _wallet_set_representative(address)


@wallet_group.command('list', short_help='list all wallets')
def wallet_list(**kwargs):
    stdout.write(wallet_service.get_table(**kwargs))


@wallet_group.command('dump', short_help='dump seed in plain text')
@click.argument('name', required=True)
def wallet_dump_seed(name):
    stdout.write(
        '\n[{0}] the seed can be used to access your funds; store it securely!\n\n'
        'enter wallet password to proceed.\n'.format(stylize('WARNING', color='yellow', bold=True))
    )
    password = password_input(validate_confirm=False)
    seed = wallet_service.get_one(raise_on_empty=True, name=name).seed
    return _dump_seed(seed, password)
