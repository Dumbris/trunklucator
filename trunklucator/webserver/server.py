"""This module contains WebServer class
    TODO DOC
"""

import os
import sys
import asyncio
import logging
from aiohttp import web
from aiohttp import WSCloseCode
import aiohttp_jinja2
import jinja2
import json
import weakref

import trunklucator.const.msg as const_msg
import trunklucator.protocol.dto as dto

logger = logging.getLogger(__name__)
#logger.addHandler(logging.NullHandler())


API_VERSION = 'v1.0'
API_URL = '/trunklucator' + '/' + API_VERSION

PRINT_MSG = logger.isEnabledFor(logging.DEBUG)

KEY_SOCKETS = 'sockets'

def prt_msg(str_:str):
    logger.debug("<-- {}".format(str_))
    return str_

DEFAUT_FRONTEND = 'html_field'

def check_frontend_dir_with_priority(frontend_dir):
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    if not frontend_dir:
        frontend_dir = DEFAUT_FRONTEND
    dirs = [
        frontend_dir, #user's local path
        os.path.join(_ROOT, os.pardir, 'frontend', frontend_dir), #user option 'label_studio'
        os.path.join(_ROOT, os.pardir, frontend_dir), 
    ]
    for _dir in dirs:
        if os.path.isdir(_dir):
            return _dir
    return None

HOST = 'HOST'
PORT = 'PORT'
FRONTEND_DIR    = 'FRONTEND_DIR'
DATA_DIR        = 'DATA_DIR'
LOG_MESSAGES    = 'LOG_MESSAGES'
CONTEXT         = 'CONTEXT'

def read_env(key, default):
    if key in os.environ:
        logger.info("Override setting using environment variable {}".format(key))
        return os.environ[key]
    return default


class WebServer:
    """WebServer class doc TODO
    """
    def __init__(self, 
                 loop=None, 
                 host='127.0.0.1', 
                 port=8086, 
                 frontend_dir=None, 
                 data_dir=None, 
                 log_messages=False, 
                 context=None
                 ):
        """ Parameters
            ----------
            loop : asyncio event loop
            host : string (optional, default is 127.0.0.1)
            port : int (optional, default is 8085)
            frontend_dir : path to frontend directory (without index.html)
            data_dir : path to /data directory for http access
        """
        self._loop = loop
        self.host = read_env(HOST, host)
        self.port = read_env(PORT, port)
        self.app = web.Application(loop=self._loop)
        self.app_runner = None
        self.data_dir = read_env(DATA_DIR, data_dir)
        self.log_messages = read_env(LOG_MESSAGES, log_messages)
        self.context = read_env(CONTEXT, context)
        #states
        self.app[KEY_SOCKETS] = weakref.WeakSet()
        self.app['task'] : dto.Data = None
        self.app['update'] : dto.Update = None
        self.app['solution_event'] = None
        #end of states
        #setup handlers
        self.app.router.add_routes(
            [
                web.get(API_URL, self.wshandle), 
                web.get('/', self.index_handler), 
                web.get('/index.html', self.index_handler), 
                web.get('/index.htm', self.index_handler), 
                web.get(r'/api/projects/{id:\d+}/next', self.get_task_handler, allow_head=False), 
                web.post(r'/api/tasks/{id:\d+}/completions/', self.post_completion_handler)
            ]
        )
        if self.data_dir:
            self.app.router.add_static('/data', self.data_dir, name='data', show_index=True)
            logger.info("Using {} as data directory.".format(self.data_dir))
        #Environment var has priority
        frontend_dir = read_env(FRONTEND_DIR, frontend_dir)
        #Frontend dir: 1) Check if local dir exists else use dir from package
        self.frontend_dir = check_frontend_dir_with_priority(frontend_dir)
        logger.info("Using {} as frontend directory.".format(self.frontend_dir))
        self.app.router.add_static('/', self.frontend_dir, name='static', show_index=True)
        
        aiohttp_jinja2.setup(self.app, loader=jinja2.FileSystemLoader(self.frontend_dir))

    def jd(self, msg : dto.Message):
        if self.log_messages:
            return prt_msg(json.dumps(msg.to_dict()))
        return json.dumps(msg.to_dict())

    def print_msg(self, line=None):
        if not line:
            line = "Server started on http://{}:{}".format(self.host, self.port)
        print(line, file=sys.stderr)
        logger.warning(line)

    async def start_default_loop(self):
        web.run_app(self.app, host=self.host, port=self.port)
        self.print_msg()

    async def start(self):
        #set up handlers
        self.app.on_shutdown.append(self.on_shutdown)
        self.app['solution_event'] = asyncio.Event()

        self.app_runner = web.AppRunner(self.app)
        await self.app_runner.setup()
        site = web.TCPSite(self.app_runner, host=self.host, port=self.port)
        await site.start()
        #self._loop.create_task(self.ask_())
        self.print_msg()

    async def stop(self):
        for ws in self.app['sockets']:
            await ws.send_str(self.jd(dto.Message(const_msg.TYPE_STOP)))
        await self.app_runner.cleanup()

    async def index_handler(self, request):
        """Redirect / to index.html

        """
        context = {'context': self.context}
        response = aiohttp_jinja2.render_template('index.html',
                                              request,
                                              context)
        return response
        #return web.HTTPFound('/index.html')

    async def get_task_handler(self, request):
        if self.app["task"]:
            _id, task, _meta = self.app["task"]
            return web.json_response({**task, **{"id":_id}})
        return web.HTTPNotFound()

    async def post_completion_handler(self, request):
        str_id = request.match_info.get('id', 0)
        try:
            task_id = int(str_id)
        except ValueError as e:
            logger.exception("Invalid message from client")
            raise e
        #create solution
        task = self.app["task"]
        if task and task.task_id == task_id:
            data = await request.json()
            self.app["solution"] = data
            assert not self.app["solution_event"].is_set()
            self.app["solution_event"].set()
            return web.json_response({'id': task_id}, status=201)
        return web.HTTPInternalServerError()

    def get_nt_field(self, msg, field, default=None):
        if msg and (field in msg):
            return msg[field]
        return default

    def msg_push_task(self, reply_id=None):
        task = None
        if self.app["task"]:
            task = self.app["task"]
        return dto.Message(const_msg.TYPE_TASK, task, reply_id=reply_id)

    def msg_push_update(self):
        data = None
        if self.app["update"]:
            data = self.app["update"]
        return dto.Message(const_msg.TYPE_UPDATE, data)


    def client_msg(self, msg):
        res = dto.Message(const_msg.TYPE_ERROR, dto.Error("Nothing to do", None))
        try:
            data = json.loads(msg.data)
            client_msg = dto.Message(**data)
        except TypeError as e:
            return dto.Message(const_msg.TYPE_ERROR, dto.Error(str(e), None), reply_id=data.get(const_msg.ID, None))
        except Exception as e:
            logger.exception("Invalid message from client")
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
                logger.exception("Can't decode solution from client")
                return dto.Message(const_msg.TYPE_ERROR, dto.Error("An exception occured", None), reply_id=data[const_msg.ID])
            if sol:
                task = self.app["task"]
                if task and task.task_id == sol.task_id:
                    self.app["solution"] = sol
                    assert not self.app["solution_event"].is_set()
                    self.app["solution_event"].set()
                    return dto.Message(const_msg.TYPE_ACK, reply_id=data[const_msg.ID])
            error_msg = "{} task not found".format(sol.task_id)  # TODO This case requires support on client side.
            return dto.Message(const_msg.TYPE_ERROR, dto.Error(error_msg, None), reply_id=data[const_msg.ID])

        return res

    async def wshandle(self, request):
        ws = web.WebSocketResponse()
        request.app[KEY_SOCKETS].add(ws)
        await ws.prepare(request)
        #first message - push task if exists, and publish last update
        try:
            await ws.send_str(self.jd(self.msg_push_task()))
            await ws.send_str(self.jd(self.msg_push_update()))
            async for msg in ws:
                if self.log_messages:
                    logger.debug("\n--> {}".format(msg))
                if msg.type == web.WSMsgType.text:
                    reply = self.client_msg(msg)
                    await ws.send_str(self.jd(reply))
                elif msg.type == web.WSMsgType.binary:
                    await ws.send_bytes(msg.data)
                #elif msg.type == web.WSMsgType.close:
                #    break
        finally:
            #await asyncio.shield()
            request.app[KEY_SOCKETS].discard(ws)
            await ws.close()
        return ws

    async def on_shutdown(self, app):
        logger.debug("Call on_shutdown")
        for ws in set(app[KEY_SOCKETS]):
            await ws.close(code=WSCloseCode.GOING_AWAY, message='Server shutdown')


    async def add_task_(self, task_data: dto.Data):
        assert self.app.loop, "Server not started properly"
        self.app["task"] = task_data
        #broadcast task data to clients
        for ws in self.app[KEY_SOCKETS]:
            await ws.send_str(self.jd(self.msg_push_task()))
        #wait for solution event
        self.app['solution_event'].clear()
        logger.debug('Waiting for solution event')
        await self.app['solution_event'].wait()
        logger.debug('Solution event triggered')
        sol = self.app['solution']
        self.app['solution'] = None
        self.app["task"] = None
        return sol

    async def add_task(self, task_data: dto.Data):
        res = None
        try:
            res = await self.add_task_(task_data)
        except Exception as e:
            logger.exception("Exception during task execution")
            raise e
        return res

    async def publish_update_(self, data: dto.Data):
        if not self.app.loop:
            logger.error("Server not started properly")
        self.app["update"] = data
        #broadcast update data to clients
        for ws in self.app[KEY_SOCKETS]:
            await ws.send_str(self.jd(self.msg_push_update()))

    async def publish_update(self, data: dto.Update):
        res = None
        try:
            await self.publish_update_(data)
        except Exception as e:
            logger.exception("Exception during publishing update")
            raise e
        return res
