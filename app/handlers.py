# -*- coding: utf-8 -*-

from json import JSONDecodeError

from aiohttp import web
from cerberus import Validator

from app import storage
from app.storage import Link, NotFoundException


async def redirect(request):
    try:
        link_id = request.match_info.get('link_id', None)

        if link_id is None:
            raise web.HTTPNotAcceptable(reason='Govno')

        link = storage.get_link(link_id)
        await storage.update_link_stats(link)

        return web.HTTPFound(link.link)

    except NotFoundException:
        raise web.HTTPNotFound(reason='Wrong link id')


async def shortcut(request):
    try:
        json = await request.json()

        v = Validator({'link': {'type': 'string'}})
        if not v.validate(json):
            raise web.HTTPBadRequest(reason=v.errors)

        link = Link(link=json['link'])
        storage.insert_link(link)
        return web.json_response({"id": link.lid})

    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="This is not json")


async def get_stats(request):
    try:
        json = await request.json()

        v = Validator({'id': {'type': 'string'}})
        if not v.validate(json):
            raise web.HTTPBadRequest(reason=v.errors)

        link = storage.get_link(json['id'])
        storage.insert_link(link)
        return web.json_response(
            {"last_redirected": link.r_at, "redirects_count": link.r_count}
        )

    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="This is not json")

    except NotFoundException:
        raise web.HTTPNotFound(reason='Wrong link id')
