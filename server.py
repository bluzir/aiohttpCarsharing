import asyncio
import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web

import settings
from routes import setup_routes

logging.basicConfig(level=settings.LEVEL)


def main():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    setup_routes(app)
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(settings.TEMPLATES_ROOT))
    app.router.add_static('/static', settings.STATIC_ROOT, show_index=True)
    web.run_app(app, host='127.0.0.1', port=settings.PORT)

if __name__ == '__main__':
    main()


