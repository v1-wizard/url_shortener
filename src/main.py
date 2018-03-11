import logging.config

from aiohttp import web

import middlewares, views
from settings import LOGGER_CONF_PATH, USH_PORT


def get_application():
    app = web.Application(middlewares=[middlewares.process_error])

    app.router.add_get('/r/{link_id}', views.http.redirect)
    app.router.add_post('/shortcut', views.http.shortcut)
    app.router.add_post('/stats', views.http.get_stats)

    app.router.add_get('/admin/all_links', views.http.get_all_links)
    app.router.add_delete('/admin/all_links', views.http.purge_all)

    app.router.add_get('/ws', views.ws.handler)

    return app


if __name__ == '__main__':
    logging.config.fileConfig(LOGGER_CONF_PATH)
    app = get_application()
    web.run_app(app, port=USH_PORT)
