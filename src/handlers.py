from json import JSONDecodeError

from aiohttp import web, WSMsgType

import logic


async def redirect(request):
    link_id = request.match_info.get('link_id', None)
    return logic.redirect(link_id)


async def shortcut(request):
    try:
        json_body = await request.json()
    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    return logic.shortcut(json_body)


async def get_stats(request):
    try:
        json_body = await request.json()
    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    return logic.get_stats(json_body)


async def purge_all(request):
    try:
        json_body = await request.json()
    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    return logic.purge_all(json_body)


async def get_all_links(request):
    return logic.get_all_links()


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            resp = logic.do_ws_logic(msg.data)
            await ws.send_str(resp)
        elif msg.type == WSMsgType.ERROR:
            print('Connection closed with exception {}'.format(ws.exception()))
        elif msg.type == WSMsgType.CLOSE:
            ws.close()
        else:
            print(msg.data)

    print('Ws connection closed')
    return ws
