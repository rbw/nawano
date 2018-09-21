# -*- coding: utf-8 -*-

import privy
import crayons

from os import urandom
from sys import stdout
from texttable import Texttable
from prompt_toolkit import prompt
from libn import mrai_from_raw, mrai_to_raw

from nawano.settings import PW_MESSAGE_INFO
from nawano.validators import PasswordQualityValidator
from nawano.exceptions import NawanoError


def stylize(text, color='white', **kwargs):
    return getattr(crayons, color)(text, **kwargs).__str__()


def from_raw(amount):
    mrai = mrai_from_raw(amount)
    return mrai.rstrip('0') if float(mrai) else 0


def to_raw(amount):
    return mrai_to_raw(str(amount))


def render_table(header, body):
    t = Texttable(max_width=110)
    t.set_cols_dtype(['t'] * len(header))
    t.set_header_align(['l'] * len(header))
    t.set_deco(Texttable.HEADER | Texttable.VLINES)
    t.header(header)
    for row in body:
        t.add_row(row)

    return '\n' + t.draw() + '\n\n'


def password_input(validate_confirm=False, pw1_text='password: ', pw2_text='confirm: '):
    qv = PasswordQualityValidator() if validate_confirm else None
    if qv:
        pre_prompt = 'enter the desired password to proceed or <ctrl+d> to cancel'
        stdout.write('\n{0}\n\n{1}\n'.format('\n'.join(PW_MESSAGE_INFO), pre_prompt))

    try:
        password1 = prompt(pw1_text, is_password=True, validator=qv).encode('utf-8')

        if not validate_confirm:
            return password1

        password2 = prompt(pw2_text, is_password=True).encode('utf-8')

        if password1 != password2:
            raise NawanoError('password confirmation failed')

        return password1
    except (KeyboardInterrupt, EOFError):
        raise NawanoError('aborted')


def generate_seed():
    seed = urandom(32).hex().upper()
    return seed.encode('ascii')


def encrypt(data, password):
    return privy.hide(data, password)


def decrypt(encrypted, password):
    try:
        return privy.peek(encrypted, password)
    except ValueError:
        raise NawanoError('invalid wallet password')
