# -*- coding: utf-8 -*-

from sys import stdout
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from click.exceptions import UsageError
from nawano.exceptions import NawanoError, NoActiveWallet

from nawano.services import state_service
from nawano.settings import PROMPT_COLOR_DEPTH, HISTORY_PATH, PROMPT_STYLE
from nawano.utils import stylize
from nawano.repl import completion, completer


def get_styled_prompt():
    return [
        ('class:prompt-name', 'nawano'),
        ('class:prompt-marker', u'> '),
    ]


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
        ('class:bottom-toolbar-key', ' · available:'),
        ('class:bottom-toolbar-value', '{0}'.format(state_service.wallet_funds['available'])),
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

    while True:
        try:
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
