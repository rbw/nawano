# -*- coding: utf-8 -*-

import click

from prompt_toolkit.completion import Completer
from .completion import NawanoCompletion


class NawanoCompleter(Completer):
    def __init__(self, ctx):
        self._ctx = ctx
        self._text_before = None
        self._completion = NawanoCompletion(ctx.command)

    @property
    def _cmd_ctx(self):
        ctx = self._ctx.command.make_context('', self._completion.args, resilient_parsing=True)

        while ctx.protected_args + ctx.args and isinstance(ctx.command, click.MultiCommand):
            a = ctx.protected_args + ctx.args
            cmd = ctx.command.get_command(ctx, a[0])

            if cmd is None:
                return None

            ctx = cmd.make_context(a[0], a[1:], parent=ctx, resilient_parsing=True)

        return ctx

    @property
    def _command(self):
        return self._cmd_ctx.command if self._cmd_ctx else None

    @property
    def _query(self):
        return self._completion.args.pop() if self._completion.args and self._completion._is_within_command else ''

    def get_completions(self, document, complete_event=None):
        self._text_before = document.text_before_cursor

        try:
            self._completion.args = self._text_before
        except ValueError:
            # Invalid input, often caused by missing closing quotation.
            return []

        return self._completion.get_matches(self._query, self._command)
