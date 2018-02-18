
from aiohttp import web
from cerberus import Validator

import helpers, storage

async def redirect(request):
    link_id = request.match_info.get('link_id', None)

    try:
        link = storage.get_link(link_id)
        storage.update_link_stats(link)
        return web.HTTPFound(location=link.link)

    except storage.NotFoundException:
        raise web.HTTPNotFound()


async def shortcut(request):
    json = await helpers.get_json_from(request)
    v = Validator({
        'link': {
            'type': 'string',
            'regex': ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                      '(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        }
    })
    if not v.validate(json):
        raise web.HTTPBadRequest(reason=v.errors)

    link = storage.Link(link=json['link'])
    storage.insert_link(link)
    return web.json_response(data={'id': link.lid})


async def get_stats(request):
    json = await helpers.get_json_from(request)
    v = Validator({'id': {'type': 'string'}})
    if not v.validate(json):
        raise web.HTTPBadRequest(reason=v.errors)

    try:
        link = storage.get_link(json['id'])

    except storage.NotFoundException:
        raise web.HTTPNotFound()

    return web.json_response(
        data={'last_redirected': link.r_at, 'redirects_count': link.r_count}
    )


async def purge_all(request):
    json = await helpers.get_json_from(request)
    v = Validator({'Are you sure?': {'type': 'string'}})
    if not v.validate(json) or not json['Are you sure?'].lower() == 'yes':
        raise web.HTTPBadRequest(reason='You must confirm your action.')

    storage.purge_all()
    return web.HTTPOk()


async def get_all_links(request):
    links = storage.get_all_links()
    return web.json_response(
        data={'links': {link.lid: link.link for link in links}}
    )
