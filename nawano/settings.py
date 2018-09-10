# -*- coding: utf-8 -*-

from os import path
from prompt_toolkit.output.color_depth import ColorDepth
from prompt_toolkit.styles import Style

NAWANO_HOME = '{0}/.nawano'.format(path.expanduser('~'))
DB_PATH = '{0}/database'.format(NAWANO_HOME)
HISTORY_PATH = '{0}/history'.format(NAWANO_HOME)

# Nawano database URI
SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///{0}'.format(DB_PATH)

# URL for obtaining list of representatives
REPRESENTATIVES_URI = 'https://mynano.ninja/api/accounts/active'

PROMPT_COLOR_DEPTH = ColorDepth.ANSI_COLORS_ONLY
PROMPT_STYLE = Style([
    ('completion-menu', 'bg:ansiyellow fg:ansiblack'),
    ('completion-menu.completion.current', 'fg:ansiwhite'),
    ('completion-menu.meta.completion', 'bg:ansibrightblack fg:ansiwhite'),
    ('completion-menu.meta.completion.current', 'fg:ansiwhite'),
    ('prompt-name', 'fg:ansiwhite'),
    ('prompt-marker', 'fg:ansigreen'),
    ('validation_error', 'bg: ansiblue'),
    ('bottom-toolbar-key', 'bg:ansigray'),
    ('bottom-toolbar-value', 'bg:ansiwhite'),
    ('bottom-toolbar-pending', 'bg:ansiyellow'),
    ('bottom-toolbar-logo', 'bg:ansigreen'),
    ('bottom-toolbar', 'fg:ansiblack bg:ansiwhite'),
])

PW_MESSAGE_INFO = [
    '- Use a good mix of numbers, letters, and symbols',
    '- Avoid using one of the ten thousand most common passwords',
    '- Use a good mix of UPPER case and lower case letters)'
]

DEFAULT_CORE_SETTINGS = [
    {
        'name': 'pending_cooldown',
        'value': '30',
        'description': 'pending notification cool-down',
        'type': 'int'
    },
    {
        'name': 'balance_sync_interval',
        'value': '10',
        'description': 'balance sync interval',
        'type': 'int'
    },
    {
        'name': 'rep_sync_interval',
        'value': '50',
        'description': 'representatives sync interval',
        'type': 'int'
    },
    {
        'name': 'backend',
        'value': 'https://getcanoe.io/rpc',
        'description': 'node network relay',
        'type': 'str'
    }
]

ADDRESS_PREFIX = 'xrb'
