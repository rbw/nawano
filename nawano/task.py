# -*- coding: utf-8 -*-

import asyncio

from contextlib import suppress
from threading import Thread


class Task(Thread):
    def __init__(self, func, interval, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._func = func
        self._interval = interval
        self._loop = None
        self._poll_task = None

    def run(self):
        self._loop = asyncio.new_event_loop()
        loop = self._loop
        asyncio.set_event_loop(loop)

        try:
            # create
            self._poll_task = asyncio.ensure_future(self._poll())

            # run
            loop.run_forever()
            loop.run_until_complete(loop.shutdown_asyncgens())

            # cancel
            self._poll_task.cancel()
            with suppress(asyncio.CancelledError):
                loop.run_until_complete(self._poll_task)
        finally:
            loop.close()

    def stop(self):
        self._loop.call_soon_threadsafe(self._loop.stop)

    async def _poll(self):
        while True:
            self._loop.call_soon_threadsafe(self._func)
            await asyncio.sleep(self._interval)
