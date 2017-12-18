from aiohttp import web

import handlers, middlewares
from settings import USH_PORT

app = web.Application(middlewares=[middlewares.process_error])
app.router.add_get('/r/{link_id}', handlers.redirect)
app.router.add_post('/shortcut', handlers.shortcut)
app.router.add_post('/stats', handlers.get_stats)

web.run_app(app, port=USH_PORT)
