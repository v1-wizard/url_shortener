import logging
from json import JSONDecodeError

from aiohttp import web, WSMsgType

import views


logger = logging.getLogger(__name__)


async def redirect(request):
    link_id = request.match_info.get('link_id', None)
    return views.redirect(link_id)


async def shortcut(request):
    try:
        json_body = await request.json()
    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    return views.shortcut(json_body)


async def get_stats(request):
    try:
        json_body = await request.json()
    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    return views.get_stats(json_body)


async def purge_all(request):
    try:
        json_body = await request.json()
    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    return views.purge_all(json_body)


async def get_all_links(request):
    return views.get_all_links()


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            resp = views.do_ws_logic(msg.data)
            await ws.send_str(resp)
        elif msg.type == WSMsgType.ERROR:
            logger.error(
                'Connection closed with exception {}'.format(ws.exception())
            )
        elif msg.type == WSMsgType.CLOSE:
            ws.close()
        else:
            logger.error(
                'Unexpected msg type {} were received'.format(msg.type)
            )

    logger.debug('Ws connection closed')
    return ws
