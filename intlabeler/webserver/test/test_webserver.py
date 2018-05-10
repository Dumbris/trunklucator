import pytest
from intlabeler.webserver.server import WebServer
from aiohttp import web
import json
import asyncio
from pprint import pprint
import numpy as np

import intlabeler.const.msg as const_msg
import intlabeler.const.task_types as const_ttype
import intlabeler.protocol.dto as dto

WS_URL = '/echo/v1.0'

def process(ws, data):
    print(':: response:')
    pprint(data)
    print()
    # ws.send_str(input('> '))

def create_task():
    #X = np.random.rand(3,2)
    X = np.array([[1,2],[3,4],[5,6]])
    y = np.array([0,1,0])
    label_name = ['Y', 'N']
    return dto.Data(dto.get_id(), X, label_name, "Test data 1", const_ttype.BINARY, y)

async def test_hello(test_client, loop):
    ws = WebServer(loop=loop)
    ws.app["tasks"] = [create_task()]
    app = ws.app
    client = await test_client(app)
    async with client.ws_connect(WS_URL) as ws:
        req = dto.Message(const_msg.TYPE_LIST)
        await ws.send_str(json.dumps(req.to_dict()))
        async for msg in ws:
            print(msg)
            if msg.type == web.WSMsgType.text:
                process(ws, json.loads(msg.data))
                break
            elif msg.type == web.WSMsgType.closed:
                ws.close()
                print(':: closed')
                break
            elif msg.type == web.WSMsgType.error:
                print(':: error')
                break