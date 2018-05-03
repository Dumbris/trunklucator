import asyncio
import datetime
import logging
import pathlib
import aiohttp_debugtoolbar
from aiohttp import web
#from aiohttp.test_utils import unused_port

from threading import Thread, Event

class AioThread(Thread):
    def __init__(self, *args, **kwargs):
        self.server = None
        super().__init__(*args, **kwargs)
        self.log = logging.getLogger()
        logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
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
        self._loop.call_soon_threadsafe(self._loop.stop)
        self.join()


class WebServer:
    def __init__(self, loop):
        self.port = None
        self.log = logging.getLogger()
        self._loop = loop
        self.app = web.Application(loop=self._loop)
        self.app['sockets'] = []
        self.app['solutions'] = {}
        aiohttp_debugtoolbar.setup(self.app)
        self.app.router.add_routes([web.get('/hello', self.handle),
                                    web.get('/echo', self.wshandle),
                                    web.get('/n/{name}', self.handle)])
        static_folder="frontend/dist"
        self.app.router.add_static('/', static_folder, name='static', show_index=True)
        #here = pathlib.Path(__file__)

    async def start(self):
        port = 8085#unused_port()
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, '127.0.0.1', port)
        await site.start()
        #self._loop.create_task(self.ask_())
        self.port = port
        print("Server started on http://localhost:%s" % self.port)

    async def handle(self, request):
        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name + " " + str(self.port)
        return web.Response(text=text)

    async def wshandle(self, request):
        ws = web.WebSocketResponse()
        self.app["sockets"].append(ws)
        await ws.prepare(request)
        await ws.send_str("Hello!")
        async for msg in ws:
            print(msg)
            if msg.type == web.WSMsgType.text:
                self.app["solutions"]["1"] = msg.data
                await ws.send_str("Hello, {}".format(msg.data))
            elif msg.type == web.WSMsgType.binary:
                await ws.send_bytes(msg.data)
            elif msg.type == web.WSMsgType.close:
                break
        return ws

    async def ask_(self):
        end_time = self.app.loop.time() + 100.0
        while True:
            for ws in self.app['sockets']:
                await ws.send_str("Hello, {}".format("w"))

            if (self.app.loop.time() + 1.0) >= end_time:
                break
            if '1' in self.app['solutions']:
                if self.app['solutions']['1']:
                    res = self.app['solutions']['1']
                    self.app['solutions']['1'] = False
                    return res
            await asyncio.sleep(0.5)

    async def do_some_work(self, x):
        res = None
        try:
            res = await self.ask_()
        except Exception as e:
            print(e)
        return res


def entry_point():
    aiothread = AioThread()
    loop = aiothread.get_loop()
    ws = WebServer(loop=loop)
    aiothread.set_server(ws)
    aiothread.start()
    aiothread.event.wait()
    return aiothread

def run_fun(aiothread):
    #loop = aiothread.get_loop()
    timeout = 3000000
    coro = aiothread.server.do_some_work(4)
    future = aiothread.add_task(coro)
    #Make sure you wait for loop to start. Calling future.cancel() in main thread will cancel asyncio coroutine in background thread.
    try:
        result = future.result(timeout)
        print(result)
    except asyncio.TimeoutError:
        print('The coroutine took too long, cancelling the task')
        future.cancel()
    except Exception as exc:
        print('The coroutine raised an exception: {!r}'.format(exc))


if __name__ == '__main__':
    aiothread = entry_point()
    for i in range(3):
        print(i)
        run_fun(aiothread)