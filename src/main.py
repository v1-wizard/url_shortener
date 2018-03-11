import logging.config

from aiohttp import web

import handlers, middlewares
from settings import LOGGER_CONF_PATH, USH_PORT


def get_application():
    app = web.Application(middlewares=[middlewares.process_error])

    app.router.add_get('/r/{link_id}', handlers.redirect)
    app.router.add_post('/shortcut', handlers.shortcut)
    app.router.add_post('/stats', handlers.get_stats)

    app.router.add_get('/admin/all_links', handlers.get_all_links)
    app.router.add_delete('/admin/all_links', handlers.purge_all)

    app.router.add_get('/ws', handlers.websocket_handler)

    return app


if __name__ == '__main__':
    logging.config.fileConfig(LOGGER_CONF_PATH)
    app = get_application()
    web.run_app(app, port=USH_PORT)
