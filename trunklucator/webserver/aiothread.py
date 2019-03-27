import asyncio
from threading import Thread, Event


class AioThread(Thread):
    def __init__(self, *args, **kwargs):
        self.server = None
        super().__init__(*args, **kwargs)
        self._loop, self.event = None, Event()


    def run(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        if self.server:
            coro = self.server.start()
            asyncio.ensure_future(coro, loop=self._loop)
        self._loop.call_soon(self.event.set)
        self._loop.run_forever()

    def set_server(self, ws):
        self.server = ws

    def get_loop(self):
        return self._loop

    def add_task(self, coro):
        fut = asyncio.run_coroutine_threadsafe(coro, loop=self._loop)
        return fut

    def finalize(self):
        if self.server:
            future = asyncio.run_coroutine_threadsafe(self.server.stop(), loop=self._loop)
            future.result()  # wait for results
        self._loop.call_soon_threadsafe(self._loop.stop)
        self.join()
