# -*- coding: utf-8 -*-

import re
import shlex
import click
from prompt_toolkit.completion import Completion

from nawano.services import wallet_service, config_service, alias_service, rep_service, state_service
from nawano.exceptions import NoActiveWallet
from nawano.settings import RPC_BACKENDS


class NawanoCompletion(object):
    _args_text = None
    _args = None

    def __init__(self, ctx):
        self._ctx = ctx

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args_text):
        self._args_text = args_text
        self._args = shlex.split(args_text)

    @property
    def _is_within_command(self):
        return self._args_text.rstrip() == self._args_text

    @property
    def req_backends(self):
        return self._args[:2] == ['config', 'backend']

    @property
    def req_reps(self):
        if len(self.args) != 2:
            return False

        return self._args[:2] == ['wallet', 'representative']

    @property
    def req_wallets(self):
        if len(self._args) != 2:
            return False

        return self._args[0] == 'wallet' and self._args[1] in ['use', 'show', 'dump']

    @property
    def req_accounts(self):
        if len(self._args) != 2:
            return False

        return self._args[0] == 'account' and self._args[1] in ['show', 'delete']

    @property
    def req_aliases(self):
        if len(self._args) < 2:
            return False

        if self._args[0] == 'alias' and self._args[1] in ['show', 'delete']:
            return True
        elif self._args[:2] == ['funds', 'send'] and self._args[-1] == '--recipient_alias':
            return True

        return False

    @property
    def req_accounts_balances(self):
        return self._args[:2] == ['funds', 'send'] and self._args[-1] == '--account_from'

    @property
    def req_config(self):
        if len(self.args) > 1:
            return False

        return self._args[:1] == ['config']

    def _reps_formatted(self, reps):
        suggestions = self._suggest_from_objs(
            reps,
            text_key='address',
            meta_str='{weight}',
            display_key='alias'
        )

        for value, display, meta in suggestions:
            yield value, display, 'weight: {0:.3}'.format(meta)

    @property
    def _suggestions(self):
        if self.req_accounts or self.req_accounts_balances:
            try:
                accounts = state_service.get_accounts()
            except NoActiveWallet:
                return [['', 'requires an active wallet', None]]
            else:
                if accounts:
                    return self._suggest_from_objs(accounts, meta_str='{available}')
                else:
                    return [['', 'no accounts found', None]]
        elif self.req_backends:
            return RPC_BACKENDS
        elif self.req_aliases:
            aliases = alias_service.get_many()
            return self._suggest_from_objs(aliases, meta_str='{description}')
        elif self.req_wallets:
            wallets = wallet_service.get_many()
            return self._suggest_from_objs(wallets)
        elif self.req_config:
            config = config_service.get_many()
            return self._suggest_from_objs(config)
        elif self.req_reps:
            reps = rep_service.get_many()
            return self._reps_formatted(reps)

        return False

    def _get_options(self, param):
        for opt in param.opts:
            if opt in self.args:
                continue

            yield opt, None, param.help

    @staticmethod
    def _get_arguments(param):
        for opt in param.type.choices:
            yield opt, None, None

    def _get_commands(self, command):
        for c in command.list_commands(command):
            cmd = command.get_command(self._ctx, c)
            yield cmd.name, None, cmd.short_help

    @staticmethod
    def _suggest_from_objs(objs, text_key='name', meta_str=None, display_key=None):
        def matches():
            return [match.group(1) for match in re.finditer(r'{(.*?)}', meta_str or '', re.DOTALL)]

        for obj in objs:
            meta_keys = {m: getattr(obj, m) for m in matches()}
            meta = meta_str.format(**meta_keys) if meta_keys else None
            display = getattr(obj, display_key) if display_key else None
            value = getattr(obj, text_key)
            yield (value, display, meta)

    def _suggest_from_click(self, command):
        if not command:
            return

        for param in command.params:
            if param.opts[0] == self.args[-1]:
                return

        for param in command.params:
            if isinstance(param, click.Option):
                yield from self._get_options(param)
            elif isinstance(param, click.Argument) and isinstance(param.type, click.Choice):
                yield from self._get_arguments(param)
        if isinstance(command, click.MultiCommand):
            yield from self._get_commands(command)

    def get_matches(self, query, command):
        suggestions = self._suggestions or self._suggest_from_click(command)
        for text, display, meta in suggestions:
            if not text.lower().startswith(query.lower()):
                continue

            start = -len(query) if text else -1

            yield Completion(text, start, display_meta=meta, display=display)
