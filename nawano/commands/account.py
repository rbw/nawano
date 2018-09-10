# -*- coding: utf-8 -*-

import click
from sys import stdout
from nanopy.crypto import account_nano
from nawano.services import wallet_service, account_service, state_service
from nawano.status import with_status
from nawano.utils import password_input
from nawano.exceptions import NawanoError
from .root import root_group


@with_status(text='creating new account')
def _account_create(**kwargs):
    public_key = account_service.insert(**kwargs)
    msg = 'address: {0}'.format(account_nano(public_key))
    return public_key, msg


def _validate_account_name(ctx, param, value):
    if state_service.get_accounts(name=value):
        raise NawanoError('an account with this name already exists')

    return account_service.validate_name(value)


def _validate_account_idx(ctx, param, value):
    if not value:
        return

    account = wallet_service.active.get_accounts(idx=value)

    if account:
        raise NawanoError('this index is already used by account: {0}'.format(account[0].name))

    return value


@root_group.group('account', short_help='account operations')
def account_group():
    pass


@account_group.command('create', short_help='create account')
@click.option('--name', 'name', help='wallet name', callback=_validate_account_name, required=True)
@click.option('--index', 'idx', help='custom account index', callback=_validate_account_idx, required=False)
def account_create(**kwargs):
    kwargs['password'] = password_input(validate_confirm=False)
    _account_create(**kwargs)


@account_group.command('show', short_help='show wallet details')
@click.option('--name', 'name', help='account name', required=True)
@click.option('--address', 'address', help='account address', required=False)
@click.option('--index', 'index', help='account index', required=False)
def account_show(**kwargs):
    stdout.write(account_service.get_details(**kwargs))


@account_group.command('delete', short_help='delete account')
@click.option('--name', required=True)
def account_delete(**kwargs):
    stdout.write(account_service.get_one(**kwargs))


@account_group.command('list', short_help='list accounts')
def account_table(**kwargs):
    stdout.write(account_service.get_table(**kwargs))

