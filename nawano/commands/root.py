# -*- coding: utf-8 -*-

import click
from sys import stdout
from nawano import REPL_LOGO
from nawano.repl.loop import nawano_loop
from nawano.utils import stylize


@click.group(invoke_without_command=True)
@click.pass_context
def root_group(ctx):
    if ctx.invoked_subcommand is None:
        stdout.write('\n'.join(REPL_LOGO))

        tab_hint = stylize('TAB', color='yellow')
        stdout.write('use the :{0}: key for auto-completion\n\n'.format(tab_hint))

        # Start REPL
        nawano_loop(ctx)


@root_group.command('exit', short_help='exit nawano')
def exit_nawano():
    pass
