from json import JSONDecodeError

from aiohttp import web


def get_json_from(request):
    try:
        return request.json()

    except JSONDecodeError:
        raise web.HTTPNotAcceptable(reason="Invalid json")
