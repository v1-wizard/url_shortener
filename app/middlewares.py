# -*- coding: utf-8 -*-

import json

from aiohttp import web


def json_error(status, message):
    body = json.dumps({'status': status, 'message': message}).encode('utf-8')
    return web.Response(
        body=body,
        content_type='application/json',
        status=status
    )


@web.middleware
async def process_error(request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPException as ex:
        return json_error(ex.status_code, ex.reason)
