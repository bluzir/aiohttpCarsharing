import asyncio
import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import base_settings as config
from routes import setup_routes

logging.basicConfig(level=config.LEVEL)


def main():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    setup_routes(app)
    setup(app, EncryptedCookieStorage(config.SECRET_KEY))
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(config.TEMPLATES_ROOT))
    app.router.add_static('/static', config.STATIC_ROOT, show_index=True)

    web.run_app(app, host=config.HOST, port=config.PORT)

if __name__ == '__main__':
    main()


