# -*- coding: utf-8 -*-

from nawano.exceptions import ValidationError, NoRecordsFound
from nawano.utils import render_table, stylize
from .state import StateService


class NawanoService(object):
    __model__ = None
    __state__ = StateService()

    def get_one(self, raise_on_empty=False, **kwargs):
        obj = self.__model__.query(**kwargs).one_or_none()

        if not obj and raise_on_empty:
            raise NoRecordsFound

        return obj

    def get_many(self, raise_on_empty=False, **kwargs):
        objs = self.__model__.query(**kwargs).all()

        if not objs and raise_on_empty:
            raise NoRecordsFound

        return objs

    def insert(self, **data):
        return self.__model__.insert(**data)

    def update(self, _id, **data):
        return self.__model__.update(_id, **data)

    def delete(self, **kwargs):
        return self.__model__.delete(**kwargs)

    @staticmethod
    def validate_name(name, argument_name='name'):
        if not 2 <= len(name) <= 30:
            raise ValidationError('argument {0} must contain between {1}'
                                  .format(argument_name, stylize('2 and 30 characters', bold=True)))
        elif ' ' in name:
            raise ValidationError('may {0}'.format(stylize('not contain spaces', bold=True)))

        return name

    def validate_address(self, address):
        return self.__state__.network.validate_address(address)

    @staticmethod
    def funds_text(funds):
        return '\n{0}available: {1} \n{0}pending: {2}'.format(' '*2, funds['available'], funds['pending'])

    @staticmethod
    def get_highlighted(text):
        return '\n({0})'.format(text)

    @staticmethod
    def get_header(text, color='yellow'):
        return '\n[{0}]'.format(stylize(text.upper(), color=color))

    @staticmethod
    def get_count_styled(count, normal=0.0):
        if float(count) > normal:
            return stylize(count, color='yellow')

        return stylize(count, color='white')

    @staticmethod
    def _format_output(data):
        return '\n'.join(data)

    @staticmethod
    def get_text_table(table_header, table_body):
        return render_table(
            table_header,
            table_body
        )
