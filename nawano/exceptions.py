# -*- coding: utf-8 -*-


class NawanoError(Exception):
    pass


class ValidationError(NawanoError):
    pass


class UnexpectedBackendResponse(NawanoError):
    def __init__(self, message):
        self.message = message

    def __str__(self, *args, **kwargs):
        return 'backend error: {0}'.format(self.message)


class NoActiveWallet(NawanoError):
    def __str__(self, *args, **kwargs):
        return 'this operation requires an active wallet'


class NoRecordsFound(NawanoError):
    def __str__(self, *args, **kwargs):
        return 'no such object'
