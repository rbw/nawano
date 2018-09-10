# -*- coding: utf-8 -*-

import click
from prompt_toolkit import prompt
from sys import stdout

from nawano.services import wallet_service, state_service
from nawano.utils import password_input
from nawano.status import with_status
from nawano.exceptions import NoSuchWallet, NawanoError
from .root import root_group


@with_status(text='setting active wallet')
def _wallet_set_active(wallet_id):
    state_service.set_wallet(wallet_id)
    msg = 'active wallet: {0}'.format(state_service.wallet.name)
    return None, msg


@with_status(text='creating wallet')
def _wallet_create(**kwargs):
    wallet_id = wallet_service.insert(**kwargs)
    msg = 'local ID: {0}'.format(wallet_id)
    return wallet_id, msg


def _validate_wallet_name(ctx, param, value):
    if wallet_service.get_one(name=value):
        raise NawanoError('a wallet with that name already exists')

    return wallet_service.validate_name(value)


@root_group.group('wallet', short_help='wallet operations')
def wallet_group():
    pass


@wallet_group.command('create', short_help='new wallet')
@click.option('--name', 'name', help='wallet name', callback=_validate_wallet_name, required=True)
def wallet_create(**kwargs):
    kwargs['password'] = password_input(validate_confirm=True)
    stdout.write('\n')
    wallet_id, _ = _wallet_create(**kwargs)

    if prompt('switch to this wallet? [Y/n] ').lower() in ['', 'y']:
        _wallet_set_active(wallet_id)


@wallet_group.command('use', short_help='set active wallet')
@click.argument('name', required=True)
def wallet_set_active(name):
    wallet = wallet_service.get_one(name=name, raises=NoSuchWallet)
    return _wallet_set_active(wallet.id)


@wallet_group.command('show', short_help='wallet details')
@click.argument('name', required=True)
def wallet_show(**kwargs):
    stdout.write(wallet_service.get_details(**kwargs))


@wallet_group.command('representative', short_help='set representative for accounts in this wallet')
@click.argument('name', required=True)
def wallet_set_representative(**kwargs):
    stdout.write('hello')


@wallet_group.command('list', short_help='wallet list')
def wallet_list(**kwargs):
    stdout.write(wallet_service.get_table(**kwargs))

