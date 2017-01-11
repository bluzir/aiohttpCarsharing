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
        self.render("registration.html", just_registered=False, alert=None)

    async def post(self):
        email = self.get_argument('email', None)
        password = self.get_argument('password', None)

        if email is None or password is None:
            self.render('registration.html', alert='Email and password must not be blank.')
            return


        try:
            await self.application.objects.create(Users,
                                      email=email,
                                      password=password)

            self.render('registration.html', alert='Successfully registered')
        except Exception as e:
             return self.render('registration.html', alert=str(e))



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
