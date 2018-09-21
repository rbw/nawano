# -*- coding: utf-8 -*-

import click
from sys import stdout
from libn import account_get
from nawano.services import account_service, state_service
from nawano.status import with_status
from nawano.utils import password_input
from nawano.exceptions import NawanoError
from .root import root_group


@with_status(text='creating new account')
def _account_create(**kwargs):
    public_key = account_service.insert(**kwargs)
    account_service.refresh_balances()
    msg = 'address: {0}'.format(account_get(public_key))
    return public_key, msg


@with_status(text='deleting account')
def _account_delete(**kwargs):
    account = account_service.get_one(raise_on_empty=True, **kwargs)
    account_service.delete(**kwargs)
    msg = 'deleted: {0}/{1}'.format(account.name, account_get(account.public_key))
    return None, msg


def _validate_account_name(ctx, param, value):
    if state_service.get_accounts(name=value):
        raise NawanoError('an account with that name already exists')

    return account_service.validate_name(value)


def _validate_account_idx(ctx, param, value):
    if not value:
        return

    account = state_service.get_accounts(idx=value)

    if account:
        raise NawanoError('this index already belongs to account: {0}'.format(account[0].name))

    return value


@root_group.group('account', short_help='account operations')
def account_group():
    assert state_service.wallet


@account_group.command('create', short_help='create account')
@click.option('--name', 'name', help='wallet name', callback=_validate_account_name, required=True)
@click.option('--index', 'idx', help='custom account index', callback=_validate_account_idx, required=False)
def account_create(**kwargs):
    kwargs['password'] = password_input(validate_confirm=False)
    _account_create(**kwargs)


@account_group.command('show', short_help='show wallet details')
# @click.option('--name', 'name', help='account name', required=False)
# @click.option('--address', 'address', help='account address', required=False)
# @click.option('--index', 'idx', help='account index', required=False)
@click.argument('name', required=True)
def account_show(**kwargs):
    # if not any([kwargs['name'], kwargs['address'], kwargs['idx']]):
    #     raise NawanoError('you must provide name, address or index')
    # kwargs['public_key'] = nano_account(kwargs.pop('address')) if kwargs['address'] else None
    stdout.write(account_service.get_details(**kwargs))


@account_group.command('delete', short_help='delete account')
@click.argument('name', required=True)
def account_delete(**kwargs):
    return _account_delete(**kwargs)


@account_group.command('list', short_help='list accounts')
def account_table(**kwargs):
    stdout.write(account_service.get_table(**kwargs))

