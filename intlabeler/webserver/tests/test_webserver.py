import pytest
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


from aiohttp.test_utils import TestClient, loop_context
from aiohttp import request

# loop_context is provided as a utility. You can use any
# asyncio.BaseEventLoop class in it's place.
with loop_context() as loop:
    app = _create_example_app()
    with TestClient(app, loop=loop) as client:

        async def test_get_route():
            nonlocal client
            resp = await client.get("/")
            assert resp.status == 200
            text = await resp.text()
            assert "Hello, world" in text

        loop.run_until_complete(test_get_route())