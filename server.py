import asyncio
import logging
import ssl

import aiohttp_jinja2
import jinja2
from aiohttp import web

from config import base_settings as config
from routes import setup_routes

logging.basicConfig(level=config.LEVEL)


def main():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    setup_routes(app)
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(config.TEMPLATES_ROOT))
    app.router.add_static('/static', config.STATIC_ROOT, show_index=True)
    if config.CRT_ROOT and config.KEY_ROOT:
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sslcontext.load_cert_chain(config.CRT_ROOT, config.KEY_ROOT)
        web.run_app(app, host=config.HOST, port=config.PORT, ssl_context=sslcontext)
    else:
        web.run_app(app, host=config.HOST, port=config.PORT)

if __name__ == '__main__':
    main()


