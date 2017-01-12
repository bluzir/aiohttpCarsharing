import asyncio
import logging
import os

import peewee_async
import tornado
from tornado.platform.asyncio import AsyncIOMainLoop

import settings
from handlers import MainHandler, RegistrationHandler, GetUserByIDHandler

logging.basicConfig(level=settings.LEVEL)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/registration", RegistrationHandler),
            (r"/user/([0-9]+)", GetUserByIDHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


def main():
    # Setting up Tornado application on asyncio
    AsyncIOMainLoop().install()
    app = Application()
    app.listen(settings.PORT)

    # Setting up Tornado database
    app.db = peewee_async.PostgresqlDatabase(settings.DB_NAME, user=settings.DB_USER)
    app.db.set_allow_sync(False)
    app.objects = peewee_async.Manager(app.db)


    # Run loop
    logging.info('Running server on port {}'.format(settings.PORT))
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print(" server stopped")


if __name__ == "__main__":
    main()