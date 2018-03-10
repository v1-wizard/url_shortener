import json

from aiohttp import web
from cerberus import Validator

import storage


def redirect(link_id):
    try:
        link = storage.get_link(link_id)
        storage.update_link_stats(link)
        return web.HTTPFound(location=link.link)
    except storage.NotFoundException:
        raise web.HTTPNotFound()


def shortcut(json_body):
    v = Validator({
        'link': {
            'type': 'string',
            'regex': ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                      '(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
            'empty': False,
            'required': True,
        },
    })
    if not v.validate(json_body):
        raise web.HTTPBadRequest(reason=v.errors)

    link = storage.Link(link=json_body['link'])
    storage.insert_link(link)
    return web.json_response(data={'id': link.lid})


def get_stats(json_body):
    v = Validator({'id': {'type': 'string', 'empty': False, 'required': True}})
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
    v = Validator({
        'confirm': {
            'type': 'string',
            'empty': False,
            'required': True,
            'allowed': ['yes', 'Yes', 'YES']
        },
    })
    if not v.validate(json_body):
        raise web.HTTPBadRequest(reason=v.errors)

    storage.purge_all()
    return web.json_response(data={})


def get_all_links(json_body=None):
    links = storage.get_all_links()
    return web.json_response(
        data={'links': {link.lid: link.link for link in links}}
    )


def do_ws_logic(websocket_msg):
    try:
        msg_type, msg_body = _validate_and_extract_from(websocket_msg)
        action = _LOGIC_MAPPER[msg_type]
        http_resp = action(msg_body)
        return _convert_to_ws_msg(http_resp)
    except web.HTTPError as err:
        return _convert_to_ws_err_msg(err)


_LOGIC_MAPPER = {
    'shortcut': shortcut,
    'get_stats': get_stats,
    'purge_all': purge_all,
    'get_all_links': get_all_links,
}


def _validate_and_extract_from(ws_msg):
    try:
        json_data = json.loads(ws_msg)
    except json.JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")

    v = Validator({
        'type': {
            'type': 'string',
            'empty': False,
            'required': True,
            'allowed': list(_LOGIC_MAPPER.keys()),
        },
        'body': {
            'type': 'dict',
            'required': True,
        },
    })

    if not v.validate(json_data):
        raise web.HTTPBadRequest(reason=v.errors)

    return json_data['type'], json_data['body']


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
