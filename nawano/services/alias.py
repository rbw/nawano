# -*- coding: utf-8 -*-

from nawano.models import Alias
from ._base import NawanoService


class AliasService(NawanoService):
    __model__ = Alias

    @staticmethod
    def _get_table_body(aliases):
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
        alias = self.get_one(raise_on_empty=True, **kwargs)

        return self._format_output([
            self.get_header('alias'),
            'name: ' + alias.name,
            'address: ' + alias.address,
            'description: {0}'.format(alias.description)
        ]) + '\n\n'

    def get_table(self, **kwargs):
        aliases = self.get_many(raise_on_empty=True, **kwargs)
        return self.get_text_table(self._table_header, self._get_table_body(aliases))
