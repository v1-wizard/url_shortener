import json
import logging

from aiohttp import web, WSMsgType
from cerberus import Validator

from . import base
import schemas


__all__ = ('handler',)
logger = logging.getLogger(__name__)


async def handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            try:
                command, body = _validate_and_extract_from(msg.data)
                action = _LOGIC_MAPPER[command]
                http_resp = await action(body)
                resp = _convert_to_ws_msg(http_resp)
            except web.HTTPError as err:
                resp = _convert_to_ws_err_msg(err)

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


_LOGIC_MAPPER = {
    'shortcut': base.shortcut,
    'get_stats': base.get_stats,
    'purge_all': base.purge_all,
    'get_all_links': base.get_all_links,
}


def _validate_and_extract_from(ws_msg):
    try:
        json_data = json.loads(ws_msg)
    except json.JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    v = Validator(schemas.WEB_SOCKET_MSG)
    if not v.validate(json_data):
        raise web.HTTPBadRequest(reason=v.errors)

    return json_data['command'], json_data['body']


def _convert_to_ws_err_msg(err):
    return json.dumps({
        'code': err.status,
        'error': err.reason
    })


def _convert_to_ws_msg(http_resp):
    return json.dumps({
        'code': http_resp.status,
        'body': json.loads(http_resp.text)
    })
