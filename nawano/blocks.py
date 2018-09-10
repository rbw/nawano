# -*- coding: utf-8 -*-

import uuid

from binascii import unhexlify, Error
from marshmallow import Schema, fields, validate, ValidationError

from nanopy.crypto import nano_account


def validate_address(address):
    try:
        nano_account(address)
    except ValueError as e:
        raise ValidationError(e)

    return True


def validate_blockhash(block_hash):
    if len(block_hash) != 64:
        raise ValidationError('invalid head block size')

    try:
        unhexlify(block_hash)
    except Error as err:
        raise ValidationError(str(err))


class StateBlock(Schema):
    type = fields.String(
        missing='state',
        required=True,
        validate=[
            validate.Equal('state')
        ]
    )

    representative = fields.String(
        required=True,
        validate=[
            validate_address
        ]
    )

    account = fields.String(
        required=True,
        validate=[
            validate_address
        ]
    )

    # id = fields.String(missing=uuid.uuid4().__str__())
    balance = fields.Integer(required=True)
    previous = fields.String(missing='0'*64, required=True, validate=[validate_blockhash])
    work = fields.String()
    signature = fields.String()


class ReceiveBlock(StateBlock):
    link = fields.String(required=True, validate=[validate_blockhash])


class OpenBlock(ReceiveBlock):
    link = fields.String(required=True, validate=[validate_blockhash])


class ChangeBlock(StateBlock):
    link = fields.String(missing='0' * 64, required=True, validate=[validate.Equal('0')])


class SendBlock(StateBlock):
    link = fields.String(required=True, validate=[validate_address])


