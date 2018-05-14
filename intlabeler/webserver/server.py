"""This module contains WebServer class
    TODO DOC
"""

import asyncio
import datetime
import logging
import pathlib
from aiohttp import web
import json
from typing import List

import intlabeler.const.msg as const_msg
import intlabeler.const.payload as const_pl
import intlabeler.protocol.dto as dto


API_VERSION = 'v1.0'
API_URL = '/echo' + '/' + API_VERSION


def jd(msg : dto.Message):
    return json.dumps(msg.to_dict())

class WebServer:
    """WebServer class doc TODO
    """
    def __init__(self, loop=None, host='127.0.0.1', port=8085, debugtoolbar=False):
        """ Parameters
            ----------
            loop : asyncio event loop
            host : string (optional, default is 127.0.0.1)
            port : int (optional, default is 8085)
            debugtoolbar : bool (default True) turn on aiohttp debugtoolbar
        """
        self._loop = loop
        self.host = host
        self.port = port
        self.log = logging.getLogger()
        self.app = web.Application(loop=self._loop)
        #states
        self.app['sockets'] = []
        self.app['tasks'] : List[dto.Data] = []
        self.app['solutions'] = {}
        #end of states
        if debugtoolbar:
            import aiohttp_debugtoolbar
            aiohttp_debugtoolbar.setup(self.app)
        #setup handlers
        self.app.router.add_routes([web.get(API_URL, self.wshandle)])
        static_folder="frontend/dist"
        self.app.router.add_static('/', static_folder, name='static', show_index=True)
        #here = pathlib.Path(__file__)

    async def start2(self):
        web.run_app(self.app, host=self.host, port=self.port)
        print("Server started on http://%s:%s" % (self.host, self.port))

    async def start(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, host=self.host, port=self.port)
        await site.start()
        #self._loop.create_task(self.ask_())
        print("Server started on http://localhost:%s" % self.port)

    #TODO move to specific module
    def list_tasks(self):
        return [t.task_id for t in self.app["tasks"]]
    
    def get_task_byid(self, task_id: str):
        try:
            return next(t for t in self.app["tasks"] if t.task_id == task_id)
        except StopIteration:
            pass
        except Exception as e:
            print(e)
        return False
    
    def get_nt_field(self, msg, field, default=None):
        if msg and (field in msg):
            return msg[field]
        return default

    def msg_push_task(self, reply_id=None):
        task = None
        if len(self.app["tasks"]) > 0:
            task = self.app["tasks"][0]
        return dto.Message(const_msg.TYPE_TASK, task, reply_id=reply_id)


    def client_msg(self, msg):
        res = dto.Message(const_msg.TYPE_ERROR, dto.Error("Nothing to do", None))
        try:
            data = json.loads(msg.data)
            client_msg = dto.Message(**data)
        except TypeError as e:
            return dto.Message(const_msg.TYPE_ERROR, dto.Error(str(e), None), reply_id=data.get(const_msg.ID, None))
        except Exception as e:
            print(e)
            raise e
        #List tasks request
        if client_msg.type == const_msg.TYPE_LIST:
            return dto.Message(const_msg.TYPE_LIST, self.list_tasks())
        #Get task request
        if client_msg.type == const_msg.TYPE_TASK:
            return self.msg_push_task(data)
        #Client post solution
        if client_msg.type == const_msg.TYPE_SOLUTION:
            #create solution
            try:
                sol = dto.Solution(**data[const_msg.PAYLOAD])
            except TypeError as e:
                return dto.Message(const_msg.TYPE_ERROR, dto.Error(str(e), None), reply_id=data[const_msg.ID])
            except Exception as e:
                print(e)
                return dto.Message(const_msg.TYPE_ERROR, dto.Error("An exception occured", None), reply_id=data[const_msg.ID])
            if sol:
                task = self.get_task_byid(sol.task_id)
                if task:
                    return dto.Message(const_msg.TYPE_ACK, reply_id=data[const_msg.ID])
            error_msg = "{} task not found".format(sol.task_id)
            return dto.Message(const_msg.TYPE_ERROR, dto.Error(error_msg, None), reply_id=data[const_msg.ID])

        return res

    async def wshandle(self, request):
        ws = web.WebSocketResponse()
        self.app["sockets"].append(ws)
        await ws.prepare(request)
        #first message - push task if exists
        await ws.send_str(jd(self.msg_push_task()))
        async for msg in ws:
            if msg.type == web.WSMsgType.text:
                reply = self.client_msg(msg)
                #print(reply.to_dict())
                await ws.send_str(json.dumps(reply.to_dict()))
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
            await asyncio.sleep(1.5)

    async def do_some_work(self, x):
        res = None
        try:
            res = await self.ask_()
        except Exception as e:
            print(e)
        return res
