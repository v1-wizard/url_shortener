from json import JSONDecodeError

from aiohttp import web
from cerberus import Validator

import storage


async def redirect(request):
    link_id = request.match_info.get('link_id', None)

    try:
        link = storage.get_link(link_id)
        storage.update_link_stats(link)
        return web.HTTPFound(location=link.link)

    except storage.NotFoundException:
        raise web.HTTPNotFound()


async def shortcut(request):
    try:
        json = await request.json()

    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    v = Validator({'link': {'type': 'string'}})
    if not v.validate(json):
        raise web.HTTPBadRequest(reason=v.errors)

    link = storage.Link(link=json['link'])
    storage.insert_link(link)
    return web.json_response(data={"id": link.lid})


async def get_stats(request):
    try:
        json = await request.json()

    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    v = Validator({'id': {'type': 'string'}})
    if not v.validate(json):
        raise web.HTTPBadRequest(reason=v.errors)

    try:
        link = storage.get_link(json['id'])

    except storage.NotFoundException:
        raise web.HTTPNotFound()

    return web.json_response(
        data={"last_redirected": link.r_at, "redirects_count": link.r_count}
    )
