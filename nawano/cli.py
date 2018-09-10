# -*- coding: utf-8 -*-

from sys import argv, exit, hexversion, stdout
from os import path, makedirs, mknod
from nawano.utils import stylize
from nawano.models import meta_create_all, State
from nawano.commands import cli
from nawano.status import with_status
from nawano.settings import NAWANO_HOME, HISTORY_PATH, DEFAULT_CORE_SETTINGS
from nawano.services import config_service, state_service


@with_status(text='creating home')
def _home_create():
    makedirs(NAWANO_HOME)


@with_status(text='touching history')
def _history_touch():
    mknod(HISTORY_PATH)


@with_status(text='seeding database')
def _database_seed():
    meta_create_all()
    State.install()
    for attr in DEFAULT_CORE_SETTINGS:
        config_service.insert(**attr)


def run():
    if hexversion < 0x03050000:
        exit('Nawano requires Python 3.5 or newer')

    if len(argv) > 1:
        exit("Nawano doesn't take arguments")

    if not path.exists(NAWANO_HOME):
        stdout.write('\n## first-time run, installing in {0}\n'
                     .format(stylize(NAWANO_HOME, color='white', bold=True)))

        _home_create()
        _history_touch()
        _database_seed()

    state_service.is_syncing = False

    # Invoke CLI
    cli(prog_name='nawano')


if __name__ == '__main__':
    run()
