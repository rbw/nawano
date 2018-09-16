# -*- coding: utf-8 -*-

from datetime import datetime
from nawano.db import get_db_session, filter_empty


class BaseMixin(object):
    big_bang = datetime.fromtimestamp(-2147483648)

    @classmethod
    def _query(cls, *entities, **kwargs):
        with get_db_session() as s:
            return s.query(entities or cls).filter_by(**filter_empty(kwargs))

    @classmethod
    def _update(cls, instance, **kwargs):
        with get_db_session() as s:
            for k, v in kwargs.items():
                setattr(instance, k, v)

            s.merge(instance)
            s.commit()

    @classmethod
    def _add(cls, instance):
        with get_db_session() as s:
            s.add(instance)
            s.commit()
