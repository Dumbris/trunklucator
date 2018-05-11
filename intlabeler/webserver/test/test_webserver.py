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

def jd(msg : dto.Message):
    return json.dumps(msg.to_dict())

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

def parse_msg(data) -> dto.Message:
    try:
        data_ = json.loads(data)
        return dto.Message(**data_)
    except TypeError as e:
        raise e
    except Exception as e:
        raise e

async def test_list_tasks(test_client, loop):
    ws = WebServer(loop=loop)
    task1 = create_task()
    ws.app["tasks"] = [task1]
    app = ws.app
    client = await test_client(app)
    async with client.ws_connect(WS_URL) as ws:
        req = dto.Message(const_msg.TYPE_LIST)
        await ws.send_str(json.dumps(req.to_dict()))
        async for ws_msg in ws:
            if ws_msg.type == web.WSMsgType.text:
                msg = parse_msg(ws_msg.data)
                if msg.type == const_msg.TYPE_LIST:
                    tasks_list = msg.payload
                    assert len(tasks_list) == 2
                if msg.type == const_msg.TYPE_TASK:
                    task2 = dto.Data(**msg.payload)
                    assert task1.task_id == task2.task_id
                    reply = dto.Message(const_msg.TYPE_SOLUTION, create_solution(), msg_id=dto.get_id())
                break
            elif ws_msg.type == web.WSMsgType.closed:
                ws.close()
                print(':: closed')
                break
            elif ws_msg.type == web.WSMsgType.error:
                print(':: error')
                break


async def test_push_task(test_client, loop):
    ws = WebServer(loop=loop)
    task1 = create_task()
    ws.app["tasks"] = [task1]
    app = ws.app
    client = await test_client(app)
    async with client.ws_connect(WS_URL) as ws:
        async for ws_msg in ws:
            if ws_msg.type == web.WSMsgType.text:
                msg = parse_msg(ws_msg.data)
                if msg.type == const_msg.TYPE_ACK:
                    assert msg.reply_id == dto.get_id()
                    print(msg)
                if msg.type == const_msg.TYPE_TASK:
                    print(msg)
                    task2 = dto.Data(**msg.payload)
                    assert task1.task_id == task2.task_id
                    assert len(task1.x) == len(task2.x)
                    await asyncio.sleep(0.5)
                    await ws.send_str(jd(dto.Message(const_msg.TYPE_SOLUTION, create_solution(), msg_id=dto.get_id())))
                break
            elif ws_msg.type == web.WSMsgType.closed:
                ws.close()
                print(':: closed')
                break
            elif ws_msg.type == web.WSMsgType.error:
                print(':: error')
                break