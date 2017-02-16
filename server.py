import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from config import base_settings as config
from routes import setup_routes


app = web.Application()
setup_routes(app)
setup(app, EncryptedCookieStorage(config.SECRET_KEY))
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(config.TEMPLATES_ROOT))
app.router.add_static('/static', config.STATIC_ROOT, show_index=True)
