# -*- coding: utf-8 -*-

import requests
from simplejson.scanner import JSONDecodeError

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
                .filter(self.__model__.weight < max_weight * 0.9)
                .order_by(Representative.weight.asc())
                .order_by(Representative.uptime.desc())
                .all()
        )

    def refresh_reps(self):
        # @TODO - look into bulk upserts with SQA
        try:
            representatives = requests.get(REPRESENTATIVES_URI).json()
        except JSONDecodeError:
            # @TODO - log error
            return False

        with get_db_session() as s:
            for rep in representatives:
                if 'alias' not in rep:
                    continue

                rep['weight'] = str(rep.pop('votingweight'))[:4]
                rep['address'] = rep.pop('account')

                existing = self.get_one(address=rep['address'])

                if not existing:
                    rep = Representative(**rep)
                    s.add(rep)
                else:
                    for k, v in rep.items():
                        setattr(existing, k, v)

                    s.merge(existing)

                s.flush()

            s.commit()

        # self.__state__.get_active_wallet.cache_clear()
