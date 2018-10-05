# -*- coding: utf-8 -*-

from sys import stdout
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from click.exceptions import UsageError
from nawano.exceptions import NawanoError

from nawano.services import account_service, rep_service
from nawano.settings import PROMPT_COLOR_DEPTH, HISTORY_PATH, PROMPT_STYLE
from nawano.utils import stylize
from nawano.task import tasks_start
from nawano.repl import (
    completion, completer, get_cfg,
    cooldown_reached, weight_announce, pending_announce,
    get_styled_prompt, get_bottom_toolbar
)


def nawano_loop(ctx):
    # Start worker threads
    tasks = tasks_start(
        [
            [account_service.refresh_balances, get_cfg('balance_refresh')],
            [rep_service.refresh_reps, get_cfg('reps_refresh') * 60]
        ]
    )

    session = PromptSession(
        completer=completer.NawanoCompleter(ctx),
        refresh_interval=1,
        color_depth=PROMPT_COLOR_DEPTH,
        history=FileHistory(HISTORY_PATH),
        style=PROMPT_STYLE,
    )

    while True:
        try:
            if cooldown_reached('pending'):
                pending_announce()

            if cooldown_reached('weight'):
                weight_announce()

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
        except (UsageError, NawanoError) as e:
            if isinstance(e, UsageError):
                msg = e.format_message()
            else:
                msg = str(e)

            stdout.write('{0} {1}\n\n'.format(stylize('>', color='red'), msg.lower()))
        except SystemExit:
            pass

    # Stop worker threads
    for task in tasks:
        task.stop()
