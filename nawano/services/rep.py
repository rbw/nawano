# -*- coding: utf-8 -*-

import requests

from nawano.models import Representative, ConfigAttribute
from nawano.settings import REPRESENTATIVES_URI
from nawano.db import get_db_session

from ._base import NawanoService


class RepresentativeService(NawanoService):
    __model__ = Representative

    def get_many(self, **kwargs):
        max_weight = ConfigAttribute.get_one(name='max_weight').value

        return (
            self.__model__.query(**kwargs)
                .filter(self.__model__.weight < max_weight * 0.8)
                .order_by(Representative.weight.asc())
                .order_by(Representative.uptime.desc())
                .all()
        )

    def refresh_reps(self):
        representatives = requests.get(REPRESENTATIVES_URI).json()

        with get_db_session() as s:
            for rep in representatives:
                if 'alias' not in rep:
                    continue

                rep['weight'] = rep.pop('votingweight')
                rep['address'] = rep.pop('account')
                existing = self.__model__.query(address=rep['address']).one_or_none()

                if not existing:
                    rep = Representative(**rep)
                    s.add(rep)
                else:
                    for k, v in rep.items():
                        setattr(existing, k, v)

                    s.merge(existing)

                s.flush()

            s.commit()
