# -*- coding: utf-8 -*-

import re
import click
from sys import stdout
from requests.exceptions import RequestException

from nawano.services import config_service
from nawano.status import with_status
from nawano.exceptions import NawanoError
from nawano.clients import RPC
from .root import root_group


@with_status(text='testing connectivity')
def _test_backend(uri):
    try:
        client = RPC(uri)
        client.get_supply()
    except RequestException as e:
        raise NawanoError(e)


@with_status(text='update config attribute')
def _config_attribute_set(name, value):
    config_service.set(name, value)
    updated = config_service.get(name)
    msg = '{0} is now {1}'.format(updated.name, updated.value)
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
            # value = re.sub(r'https?://', '', value)
            _test_backend(value)

        _config_attribute_set(name, value)
    else:
        attr = config_service.get(name)
        stdout.write('{0}\n\n'.format(attr.value))
