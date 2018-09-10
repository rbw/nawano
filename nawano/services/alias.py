# -*- coding: utf-8 -*-

from nawano.models import Alias
from nawano.exceptions import NawanoError
from ._base import NawanoService


class AliasService(NawanoService):
    __model__ = Alias

    def _get_table_body(self, aliases):
        for m in aliases:
            yield [
                m.name,
                '…{0}'.format(m.address[-8:]),
                m.description
            ]

    @property
    def _table_header(self):
        return ['name', 'address', 'description']

    def get_details(self, **kwargs):
        alias = self.__model__.query(**kwargs).one_or_none()
        if not alias:
            raise NawanoError('no alias by that name')

        return self._format_output([
            self.get_header('alias'),
            'name: {0}'.format(alias.name),
            'address: {0}'.format(alias.address),
            'description: {0}'.format(alias.description)
        ]) + '\n\n'

    def get_table(self, **kwargs):
        aliases = self.__model__.query(**kwargs).all()
        if not aliases:
            raise NawanoError('no aliases found')

        return self.get_text_table(self._table_header, self._get_table_body(aliases))
