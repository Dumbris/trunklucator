import pytest
from intlabeler.webserver.server import WebServer
from aiohttp import web
import json
import asyncio
from pprint import pprint
from unittest.mock import patch
import numpy as np
import uuid

import intlabeler.const.msg as const_msg
import intlabeler.const.task_types as const_ttype
import intlabeler.protocol.dto as dto

WS_URL = '/echo/v1.0'

def fake_uuid():
    return patch.object(uuid, 'uuid4', side_effect=['15bfcc21-de44-47d9-9189-1f9f91453311'])

def process(ws, data):
    print(':: response:')
    pprint(data)
    print()
    # ws.send_str(input('> '))

def get_id():
    with fake_uuid():
        return dto.get_id()

def create_task():
    #X = np.random.rand(3,2)
    X = np.array([[1,2],[3,4],[5,6]])
    y = np.array([0,1,0])
    label_name = ['Y', 'N']
    return dto.Data(get_id(), X, label_name, "Test data 1", const_ttype.BINARY, y)

def create_solution():
    y = np.array([0,1,1])
    return dto.Solution(get_id(), y)

async def test_hello(test_client, loop):
    ws = WebServer(loop=loop)
    task1 = create_task()
    ws.app["tasks"] = [task1]
    app = ws.app
    client = await test_client(app)
    async with client.ws_connect(WS_URL) as ws:
        req = dto.Message(const_msg.TYPE_LIST)
        await ws.send_str(json.dumps(req.to_dict()))
        async for msg in ws:
            print(msg)
            if msg.type == web.WSMsgType.text:
                #process(ws, json.loads(msg.data))
                if msg.data[const_msg.TYPE] == const_msg.TYPE_LIST:
                    tasks_list = msg.data[const_msg.PAYLOAD]
                    assert len(tasks_list) == 2
                if msg.data[const_msg.TYPE] == const_msg.TYPE_TASK:
                    task2 = dto.Data(**msg.data[const_msg.PAYLOAD])
                    assert task1 == task2
                    reply = dto.Message(const_msg.TYPE_SOLUTION, create_solution(), msg_id=dto.get_id())
                break
            elif msg.type == web.WSMsgType.closed:
                ws.close()
                print(':: closed')
                break
            elif msg.type == web.WSMsgType.error:
                print(':: error')
                break