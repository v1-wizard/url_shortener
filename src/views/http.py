from json import JSONDecodeError

from aiohttp import web

from . import base
import storage


__all__ = ('redirect', 'shortcut', 'get_stats', 'purge_all', 'get_all_links',)


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
        json_body = await request.json()
    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    return base.shortcut(json_body)


async def get_stats(request):
    try:
        json_body = await request.json()
    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    return base.get_stats(json_body)


async def purge_all(request):
    try:
        json_body = await request.json()
    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    return base.purge_all(json_body)


async def get_all_links(request):
    return base.get_all_links()
