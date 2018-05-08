import pytest
from intlabeler.webserver.server import WebServer
from aiohttp import web

async def hello(request):
    return web.Response(text='Hello, world')

async def test_hello(test_client, loop):
    app = web.Application()
    app.router.add_get('/', hello)
    client = await test_client(app)
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello, world' in text