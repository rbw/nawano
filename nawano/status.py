# -*- coding: utf-8 -*-

from functools import wraps
from sys import stdout
from nawano.utils import stylize
from nawano.exceptions import NawanoError


class StatusMessage(object):
    l_just = 7

    def __init__(self, text):
        self._text = text

    def _create_message(self, status, color, end='\n', result=None):
        msg = '\r[{0}] {1}{2}'.format(
            stylize(status, color=color).ljust(self.l_just),
            self._text,
            end
        )

        if result is None:
            return msg

        return '{0}{1} {2}\n\n'.format(msg, stylize('>', color=color), result)

    def get_completed(self, **kwargs):
        return self._create_message('success', 'green', **kwargs)

    def get_failed(self, **kwargs):
        return self._create_message('failure', 'red', **kwargs)

    def get_working(self):
        return self._create_message('working', 'yellow', end='')


def with_status(text):
    status = StatusMessage(text)

    def inner(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                stdout.write(status.get_working())
                res = f(*args, **kwargs)
                msg = res[1] if isinstance(res, tuple) else None
                stdout.write(status.get_completed(result=msg))

                return res
            except Exception as exc:
                if isinstance(exc, NawanoError):
                    stdout.write(status.get_failed(result=str(exc)))
                    raise SystemExit

                raise

        return wrapped

    return inner
