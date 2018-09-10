# -*- coding: utf-8 -*-

import requests

from nawano.models import Representative
from nawano.settings import REPRESENTATIVES_URI
from nawano.db import get_db_session

from ._base import NawanoService


class RepresentativeService(NawanoService):
    __model__ = Representative

    def get_many(self, **kwargs):
        return (
            self.__model__.query(**kwargs)
                .order_by(Representative.weight.asc())
                .order_by(Representative.uptime.desc())
                .all()
        )

    def sync(self):
        representatives = requests.get(REPRESENTATIVES_URI).json()

        with get_db_session() as s:
            s.query(Representative).delete()

            for rep in representatives:
                if 'alias' not in rep:
                    continue
                elif int(rep['votingweight']) > 4e35:
                    continue

                rep['weight'] = rep.pop('votingweight')
                rep['address'] = rep.pop('account')
                existing = Representative.query(address=rep['address']).one_or_none()

                if not existing:
                    rep = Representative(**rep)
                    s.add(rep)
                else:
                    for k, v in rep.items():
                        setattr(existing, k, v)

                    s.merge(existing)

                s.flush()

            s.commit()


