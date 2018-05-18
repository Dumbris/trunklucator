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

PRINT_MSG = True

def prt_msg(str_:str):
    print("<-- {}".format(str_))
    return str_

def jd(msg : dto.Message):
    if PRINT_MSG:
        return prt_msg(json.dumps(msg.to_dict()))
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
        self.app_runner = None
        #states
        self.app['sockets'] = []
        #self.app['tasks'] : List[dto.Data] = []
        self.app['task'] : dto.Data = None
        self.app['solution_event'] = None
        #end of states
        if debugtoolbar:
            import aiohttp_debugtoolbar
            aiohttp_debugtoolbar.setup(self.app)
        #setup handlers
        self.app.router.add_routes([web.get(API_URL, self.wshandle)])
        static_folder="frontend/dist_simple"
        self.app.router.add_static('/', static_folder, name='static', show_index=True)
        #here = pathlib.Path(__file__)

    async def start_default_loop(self):
        web.run_app(self.app, host=self.host, port=self.port)
        print("Server started on http://%s:%s" % (self.host, self.port))

    async def start(self):
        self.app_runner = web.AppRunner(self.app)
        await self.app_runner.setup()
        site = web.TCPSite(runner, host=self.host, port=self.port)
        await site.start()
        #self._loop.create_task(self.ask_())
        print("Server started on http://localhost:%s" % self.port)

    async def stop(self):
        await self.app_runner.cleanup()

    def get_nt_field(self, msg, field, default=None):
        if msg and (field in msg):
            return msg[field]
        return default

    def msg_push_task(self, reply_id=None):
        task = None
        if self.app["task"]:
            task = self.app["task"]
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
        #Get task request
        if client_msg.type == const_msg.TYPE_TASK:
            return self.msg_push_task(client_msg.msg_id)
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
                task = self.app["task"]
                if task and task.task_id == sol.task_id:
                    self.app["solution"] = sol
                    #assert self.app["solution_event"]
                    if self.app["solution_event"]:
                        self.app["solution_event"].set()
                    return dto.Message(const_msg.TYPE_ACK, reply_id=data[const_msg.ID])
            error_msg = "{} task not found".format(sol.task_id)
            return dto.Message(const_msg.TYPE_ERROR, dto.Error(error_msg, None), reply_id=data[const_msg.ID])

        return res

    async def wshandle(self, request):
        ws = web.WebSocketResponse()
        self.app["sockets"].append(ws)
        await ws.prepare(request)
        #first message - push task if exists
        try:
            await ws.send_str(jd(self.msg_push_task()))
            async for msg in ws:
                if PRINT_MSG:
                    print("\n--> {}".format(msg))
                if msg.type == web.WSMsgType.text:
                    reply = self.client_msg(msg)
                    #print(reply.to_dict())
                    await ws.send_str(jd(reply))
                elif msg.type == web.WSMsgType.binary:
                    await ws.send_bytes(msg.data)
                elif msg.type == web.WSMsgType.close:
                    break
        finally:
            #await asyncio.shield()
            pass
        return ws

    async def add_task_(self, task_data: dto.Data):
        assert self.app.loop, "Server not started properly"
        self.app["task"] = task_data
        #broadcast task data to clients
        for ws in self.app['sockets']:
            await ws.send_str(jd(self.msg_push_task()))
        #wait for solution event
        self.app['solution_event'] = asyncio.Event()
        print('waiting for solution event\n\n')
        await self.app['solution_event'].wait()
        print('solution event triggered\n\n')
        sol = self.app['solution']
        self.app['solution'] = None
        self.app["task"] = None
        return sol

    async def add_task(self, task_data: dto.Data):
        res = None
        try:
            res = await self.add_task_(task_data)
        except Exception as e:
            raise e
        return res
