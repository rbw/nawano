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
    def _update(cls, obj, **kwargs):
        with get_db_session() as s:
            for k, v in kwargs.items():
                setattr(obj, k, v)

            s.merge(obj)
            s.commit()

    @classmethod
    def delete(cls, **kwargs):
        with get_db_session() as s:
            obj = s.query(cls).filter_by(**filter_empty(kwargs)).one()
            s.delete(obj)
            s.commit()

    @classmethod
    def _add(cls, obj):
        with get_db_session() as s:
            s.add(obj)
            s.commit()
