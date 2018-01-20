from aiohttp import web

import handlers, middlewares
from settings import USH_PORT

app = web.Application(middlewares=[middlewares.process_error])
app.router.add_get('/r/{link_id}', handlers.redirect)
app.router.add_post('/shortcut', handlers.shortcut)
app.router.add_post('/stats', handlers.get_stats)
app.router.add_delete('/admin/purge', handlers.purge_all)

web.run_app(app, port=USH_PORT)
