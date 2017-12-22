from aiohttp import web


@web.middleware
async def process_error(request, handler):
    try:
        response = await handler(request)
        return response

    except web.HTTPException as ex:
        return web.json_response(
            data={'status': ex.status_code, 'message': ex.reason},
            status=ex.status_code
        )
