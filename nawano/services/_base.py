# -*- coding: utf-8 -*-

from sqlalchemy.orm.exc import NoResultFound
from nawano.exceptions import ValidationError
from nawano.utils import render_table, stylize
from .state import StateService


class NawanoService(object):
    __model__ = None
    __state__ = StateService()

    def get_one(self, **kwargs):
        exc = kwargs.pop('raises', None)

        try:
            return self.__model__.query(**kwargs).one()
        except NoResultFound:
            if exc:
                raise exc

            return None

    def get_many(self, **kwargs):
        exc = kwargs.pop('raises', None)
        res = self.__model__.query(**kwargs).all()
        if not res and exc:
            raise exc

        return res

    def insert(self, **data):
        return self.__model__.insert(**data)

    def update(self, idx, **data):
        return self.__model__.update(idx, **data)

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

    def funds_text(self, funds):
        return '\n{0}balance: {1} \n{0}pending: {2}'.format(' '*2, funds['balance'], funds['pending'])

    def get_highlighted(self, text):
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

