# -*- coding: utf-8 -*-

import click
from sys import stdout
from requests.exceptions import RequestException

from nawano.services import config_service, rep_service
from nawano.status import with_status
from nawano.exceptions import NawanoError
from nawano.clients import RPC
from .root import root_group


@with_status(text='testing connectivity')
def _test_backend(uri):
    try:
        client = RPC(uri)
        client.get_version()
    except RequestException as e:
        raise NawanoError(e)


@with_status(text='update config attribute')
def _config_attribute_set(name, value):
    updated = config_service.set_attribute(name, value)
    msg = '{0} updated'.format(updated.name)
    return None, msg


@root_group.command('config', short_help='manage nawano config')
@click.argument('attribute', required=False)
@click.argument('value', required=False)
def config_group(attribute=None, value=None):
    name = attribute
    if not name:
        stdout.write(config_service.table)
    elif name and value:
        if name == 'backend':
            _test_backend(value)
            name = 'backend'

        _config_attribute_set(name, value)
    else:
        attr = config_service.get_attribute(name)
        stdout.write('{0}\n\n'.format(attr.value))

