from aiohttp import web
from cerberus import Validator

import storage, schemas


async def shortcut(json_body):
    v = Validator(schemas.SHORTCUT)
    if not v.validate(json_body):
        raise web.HTTPBadRequest(reason=v.errors)

    link = storage.Link(link=json_body1['link'])
    await storage.insert_link(link)
    return web.json_response(data={'id': link.lid})


async def get_stats(json_body):
    v = Validator(schemas.GET_STATS)
    if not v.validate(json_body):
        raise web.HTTPBadRequest(reason=v.errors)

    try:
        link = await storage.get_link(json_body['id'])
    except storage.NotFoundException:
        raise web.HTTPNotFound()

    return web.json_response(
        data={'last_redirected': link.r_at, 'redirects_count': link.r_count}
    )


async def purge_all(json_body):
    v = Validator(schemas.PURGE_ALL)
    if not v.validate(json_body):
        raise web.HTTPBadRequest(reason=v.errors)

    await storage.purge_all()
    return web.json_response(data={})


async def get_all_links(json_body=None):
    links = await storage.get_all_links()
    return web.json_response(
        data={'links': {link.lid: link.link for link in links}}
    )
