from aiohttp import web
from cerberus import Validator

import storage, schemas


def shortcut(json_body):
    v = Validator(schemas.SHORTCUT)
    if not v.validate(json_body):
        raise web.HTTPBadRequest(reason=v.errors)

    link = storage.Link(link=json_body['link'])
    storage.insert_link(link)
    return web.json_response(data={'id': link.lid})


def get_stats(json_body):
    v = Validator(schemas.GET_STATS)
    if not v.validate(json_body):
        raise web.HTTPBadRequest(reason=v.errors)

    try:
        link = storage.get_link(json_body['id'])
    except storage.NotFoundException:
        raise web.HTTPNotFound()

    return web.json_response(
        data={'last_redirected': link.r_at, 'redirects_count': link.r_count}
    )


def purge_all(json_body):
    v = Validator(schemas.PURGE_ALL)
    if not v.validate(json_body):
        raise web.HTTPBadRequest(reason=v.errors)

    storage.purge_all()
    return web.json_response(data={})


def get_all_links(json_body=None):
    links = storage.get_all_links()
    return web.json_response(
        data={'links': {link.lid: link.link for link in links}}
    )
