# -*- coding: utf-8 -*-

import click

from decimal import Decimal
from sys import stdout
from nawano import REPL_LOGO
from nawano.repl.loop import nawano_loop
from nawano.utils import stylize
from nawano.services import config_service, account_service, rep_service, state_service
from nawano.task import Task
from nawano.exceptions import NoActiveWallet


def pending_notify():
    try:
        funds = state_service.wallet_funds
    except NoActiveWallet:
        return

    if funds['pending'] > 0:
        stdout.write('\n- there are pending funds, use {0} to claim now.\n'.format(
            stylize('funds pull', color='yellow')
        ))


def weight_notify():
    try:
        representative = state_service.wallet.representative
        if not representative or not representative.weight:
            return
    except NoActiveWallet:
        return

    if Decimal(representative.weight) > Decimal(config_service.max_weight):
        stdout.write('\n- your representative is too heavy, use {0} to change\n'.format(
            stylize('wallet representative', color='yellow')
        ))


def tasks_start(tasks_args):
    tasks = []
    for task_args in tasks_args:
        task = Task(*task_args)
        task.start()
        tasks.append(task)

    return tasks


@click.group(invoke_without_command=True)
@click.pass_context
def root_group(ctx):
    if ctx.invoked_subcommand is None:
        stdout.write('\n'.join(REPL_LOGO))

        tab_hint = stylize('TAB', color='yellow')
        stdout.write('use the :{0}: key for auto-completion\n\n'.format(tab_hint))

        state_service.is_syncing = False

        # Start worker threads
        tasks = tasks_start(
            [
                [account_service.refresh_balances, config_service.balance_refresh_interval],
                [rep_service.refresh_reps, config_service.reps_refresh_interval],
                [pending_notify, config_service.pending_check_interval],
                [weight_notify, config_service.rep_check_interval]
            ]
        )

        # Start REPL
        nawano_loop(ctx)

        # Stop worker threads
        for task in tasks:
            task.stop()

        stdout.write('\nnawano loop stopped.. buh-bye!\n')


@root_group.command('exit', short_help='exit nawano')
def exit_nawano():
    pass
