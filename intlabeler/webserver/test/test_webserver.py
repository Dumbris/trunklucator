import pytest
from intlabeler.webserver.server import WebServer
from aiohttp import web
import json
import asyncio
from pprint import pprint

import intlabeler.const.msg as const_msg
import intlabeler.protocol.create as create

WS_URL = '/echo'

def process(ws, data):
    print(':: response:')
    pprint(data)
    print()
    # ws.send_str(input('> '))

async def test_hello(test_client, loop):
    ws = WebServer(loop=loop)
    app = ws.app
    client = await test_client(app)
    async with client.ws_connect(WS_URL) as ws:
        t = create.client_req(msg_type=const_msg.TYPE_LIST)
        await ws.send_str(json.dumps(t.to_dict()))
        async for msg in ws:
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