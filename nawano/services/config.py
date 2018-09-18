# -*- coding: utf-8 -*-

from functools import lru_cache

from nawano.models import ConfigAttribute
from nawano.exceptions import NawanoError

from ._base import NawanoService


class ConfigService(NawanoService):
    __model__ = ConfigAttribute

    @property
    def _table_header(self):
        return ['name', 'value', 'description']

    @property
    def table(self):
        return self.get_text_table(self._table_header, self._table_body)

    @property
    def _table_body(self):
        def truncate(value):
            if len(value) > 25:
                return '{0}…'.format(value[:25])

            return value

        for c in self.get_many():
            yield [
                c.name,
                truncate(c.value),
                c.description
            ]

    @lru_cache()
    def get(self, key):
        attr = self.__model__.get_one(key)
        if not attr:
            raise NawanoError('unrecognized attribute')

        return attr

    def set(self, key, value):
        attr = self.get(key)

        try:
            eval(attr.type)(value)
        except ValueError:
            raise NawanoError('unrecognized type provided for {0}'.format(attr.name))

        self.__model__.update(name=key, value=value)
        self.get.cache_clear()
