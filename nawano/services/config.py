# -*- coding: utf-8 -*-

from nawano.models import ConfigAttribute
from nawano.exceptions import NawanoError

from ._base import NawanoService

PENDING_CHECK_INTERVAL = 'pending_check'
WEIGHT_CHECK_INTERVAL = 'weight_check'
BALANCE_REFRESH_INTERVAL = 'balance_refresh'
REPS_REFRESH_INTERVAL = 'reps_refresh'
REP_MAX_WEIGHT = 'max_weight'
RPC_BACKEND = 'backend'


class ConfigService(NawanoService):
    __model__ = ConfigAttribute

    @property
    def _table_body(self):
        def truncate(value):
            if len(value) > 30:
                return '{0}…'.format(value[:30])

            return value

        for c in self.get_many():
            yield [
                c.name,
                truncate(c.value),
                c.description
            ]

    @property
    def _table_header(self):
        return ['name', 'value', 'description']

    @property
    def table(self):
        return self.get_text_table(self._table_header, self._table_body) + '\n'

    @property
    def backend(self):
        return self.get_attribute(RPC_BACKEND).value

    @backend.setter
    def backend(self, value):
        self.__set_valid_attribute(RPC_BACKEND, value=value)
        self.__state__.backend_refresh()

    @property
    def max_weight(self):
        return float(self.get_attribute(REP_MAX_WEIGHT).value)

    @max_weight.setter
    def max_weight(self, value):
        self.__set_valid_attribute(REP_MAX_WEIGHT, value=value)

    @property
    def pending_check_interval(self):
        return int(self.get_attribute(PENDING_CHECK_INTERVAL).value)

    @pending_check_interval.setter
    def pending_check_interval(self, value):
        self.__set_valid_attribute(PENDING_CHECK_INTERVAL, value=value)

    @property
    def rep_check_interval(self):
        return int(self.get_attribute(WEIGHT_CHECK_INTERVAL).value)

    @rep_check_interval.setter
    def rep_check_interval(self, value):
        self.__set_valid_attribute(WEIGHT_CHECK_INTERVAL, value=value)

    @property
    def reps_refresh_interval(self):
        return int(self.get_attribute(REPS_REFRESH_INTERVAL).value)

    @reps_refresh_interval.setter
    def reps_refresh_interval(self, value):
        if not 30 <= int(value) <= 360:
            raise NawanoError('representative refresh interval must be between 30 and 360 minutes')

        self.__set_valid_attribute(REPS_REFRESH_INTERVAL, value * 60)

    @property
    def balance_refresh_interval(self):
        return int(self.get_attribute(BALANCE_REFRESH_INTERVAL).value)

    @balance_refresh_interval.setter
    def balance_refresh_interval(self, value):
        if not 5 <= int(value) <= 120:
            raise NawanoError('balance refresh interval must be between 5 and 120 seconds')

        self.__set_valid_attribute(BALANCE_REFRESH_INTERVAL, value)

    def __set_valid_attribute(self, name, value):
        return self.update(name, value=value)

    def set_attribute(self, name, value):
        attr = self.get_attribute(name)

        try:
            eval(attr.type)(value)
        except ValueError:
            raise NawanoError('unrecognized type provided for {0}'.format(attr.name))

        setattr(self, attr.name, value)
        return self.get_attribute(name)

    def get_attribute(self, attr_name):
        attr = self.__model__.get_one(attr_name)
        if not attr:
            raise NawanoError('unrecognized attribute')

        return attr

