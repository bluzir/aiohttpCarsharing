import asyncio
import logging
import os

import peewee_async
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.platform.asyncio import AsyncIOMainLoop

from models import Users
from settings import DB_NAME, DB_USER

logging.basicConfig(level=logging.DEBUG)

PORT = 8080
DATABASE = peewee_async.PostgresqlDatabase(DB_NAME, user=DB_USER)
DATABASE.set_allow_sync(False)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/registration", RegistrationHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class RegistrationHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("registration.html")

    async def post(self):
        login = self.get_argument('login', None)
        password = self.get_argument('password', None)

        if not login or not password:
            raise tornado.web.HTTPError(401, "Something is wrong")
        else:
            user = await self.application.objects.create(Users,
                                                         login=login,
                                                         password=password)
            self.write({
                'id': user.id,
            })

def main():
    AsyncIOMainLoop().install()
    app = Application()
    app.listen(PORT)
    app.objects = peewee_async.Manager(DATABASE)
    tornado.ioloop.IOLoop.current().start()
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("server stopped")


if __name__ == "__main__":
    logging.info('Running server on port {}'.format(PORT))
    main()
