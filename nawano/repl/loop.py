# -*- coding: utf-8 -*-

from sys import stdout
from datetime import datetime
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from click.exceptions import UsageError
from nawano.exceptions import NawanoError, NoActiveWallet

from nawano.services import config_service, wallet_service, account_service, rep_service, state_service
from nawano.settings import PROMPT_COLOR_DEPTH, HISTORY_PATH, PROMPT_STYLE
from nawano.utils import stylize
from nawano.status import with_status
from nawano.repl import completion, completer
from nawano.task import Task


def get_styled_prompt():
    return [
        ('class:prompt-name', 'nawano'),
        ('class:prompt-marker', u'> '),
    ]


@with_status('stopping background threads')
def workers_stop(*tasks):
    for task in tasks:
        task.stop()

    return None, None


def get_bottom_toolbar():
    try:
        wallet = state_service.wallet
    except NoActiveWallet:
        return None

    pending_class = 'class:bottom-toolbar-pending' if state_service.wallet_funds['pending'] > 0 else 'class:bottom-toolbar-value'

    return [
        ('class:bottom-toolbar-logo', ' ⩫ '),
        ('class:bottom-toolbar-key', 'wallet:'),
        ('class:bottom-toolbar-value', '{0}'.format(wallet.name)),
        ('class:bottom-toolbar-key', ' · balance:'),
        ('class:bottom-toolbar-value', '{0}'.format(state_service.wallet_funds['balance'])),
        ('class:bottom-toolbar-key', ' · pending:'),
        (pending_class, '{0}'.format(state_service.wallet_funds['pending'])),
    ]


def nawano_loop(ctx):
    session = PromptSession(
        completer=completer.NawanoCompleter(ctx),
        refresh_interval=1,
        color_depth=PROMPT_COLOR_DEPTH,
        history=FileHistory(HISTORY_PATH),
        style=PROMPT_STYLE,
    )

    wallet_sync = Task(account_service.refresh_balances, config_service.balance_sync_interval)
    wallet_sync.start()

    rep_sync = Task(rep_service.sync, config_service.rep_sync_interval)
    rep_sync.start()

    while True:
        try:
            try:
                wallet = state_service.wallet
            except NoActiveWallet:
                wallet = None

            if wallet and state_service.wallet_funds['pending'] > 0:
                last_announced_secs = (datetime.now() - wallet.pending_announced).total_seconds()

                if last_announced_secs > config_service.pending_cooldown:
                    stdout.write('\n- there are pending funds, use {0} to claim now.\n'.format(
                        stylize('funds pull', color='yellow')
                    ))
                    wallet.pending_announced = datetime.now()

            cmd_str = session.prompt(get_styled_prompt(), bottom_toolbar=get_bottom_toolbar)

            if not cmd_str:
                continue

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        try:
            c = completion.NawanoCompletion(ctx.command)
            c.args = cmd_str
            if c.args[0] in ['exit', 'quit']:
                break
        except ValueError as e:
            stdout.write(str(e) + '\n\n')
            continue

        try:
            with ctx.command.make_context(None, c._args, parent=ctx.parent) as ctx:
                ctx.command.invoke(ctx)
                ctx.exit()
        except (UsageError, NawanoError) as e:
            if isinstance(e, UsageError):
                msg = e.format_message()
            else:
                msg = str(e)

            stdout.write('{0} {1}\n\n'.format(stylize('>', color='red'), msg.lower()))
        except SystemExit:
            pass

    workers_stop(wallet_sync, rep_sync)

    stdout.write('\nnawano stopped.. buh-bye!\n')
