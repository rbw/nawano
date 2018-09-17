# -*- coding: utf-8 -*-

import click
from sys import stdout
from nawano.services import alias_service
from nawano.status import with_status
from nawano.exceptions import NawanoError
from .root import root_group


@with_status(text='creating alias')
def _alias_create(**kwargs):
    address = alias_service.insert(**kwargs)
    msg = 'created alias {0}/{1}'.format(kwargs['name'], address)
    return address, msg


@with_status(text='deleting alias')
def _alias_delete(**kwargs):
    alias = alias_service.get_one(raise_on_empty=True, **kwargs)
    alias_service.delete(**kwargs)
    msg = 'deleted: {0}/{1}'.format(alias.name, alias.address)
    return None, msg


@with_status(text='validating address')
def _validate_address(address):
    if not alias_service.validate_address(address):
        raise NawanoError('invalid address')

    return address, None


def _validate_name(ctx, param, value):
    if alias_service.get_one(name=value):
        raise NawanoError('an alias with that name already exists')
    elif value.startswith(('xrb_', 'nano_',)):
        raise NawanoError('alias name looks like an address')

    return alias_service.validate_name(value)


def _validate_address_light(ctx, param, value):
    if not value.startswith(('xrb_', 'nano_',)):
        raise NawanoError('alias address should start with xrb_ or nano_')

    alias = alias_service.get_one(address=value)
    if alias:
        raise NawanoError('that address is already mapped to: {0}'.format(alias.name))

    return value


@root_group.group('alias', short_help='manage aliases')
def alias_group():
    pass


@alias_group.command('create', short_help='create alias')
@click.option('--name', 'name', help='alias name', callback=_validate_name, required=True)
@click.option('--address', 'address', help='alias address', callback=_validate_address_light, required=True)
@click.option('--description', 'description', help='alias description', required=False)
def alias_create(**kwargs):
    _validate_address(kwargs.get('address'))
    _alias_create(**kwargs)


@alias_group.command('show', short_help='show alias details')
# @click.option('--name', 'name', help='by name')
# @click.option('--address', 'address', help='by address')
@click.argument('name', required=True)
def alias_show(**kwargs):
    stdout.write(alias_service.get_details(**kwargs))


@alias_group.command('delete', short_help='delete alias')
@click.argument('name', required=True)
def alias_delete(**kwargs):
    # stdout.write(alias_service.get_one(**kwargs))
    return _alias_delete(**kwargs)


@alias_group.command('list', short_help='list aliases')
def alias_table(**kwargs):
    stdout.write(alias_service.get_table(**kwargs))

