import asyncio

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import setting as config
from route import setup_routes

import logging

from model.payment import PaymentStatus
logging.basicConfig(filename='log/main.log', level=logging.DEBUG)


app = web.Application()
setup_routes(app)
setup(app, EncryptedCookieStorage(config.SECRET_KEY))
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(config.TEMPLATES_ROOT))
app.router.add_static('/static', config.STATIC_ROOT, show_index=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    setup_routes(app)
    setup(app, EncryptedCookieStorage(config.SECRET_KEY))
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(config.TEMPLATES_ROOT))
    app.router.add_static('/static', config.STATIC_ROOT, show_index=True)
    web.run_app(app, host=config.HOST, port=config.PORT)
