import asyncio
import logging

import peewee_async
import tornado
from tornado.platform.asyncio import AsyncIOMainLoop

import settings as config
from urls import url_patterns

logging.basicConfig(level=config.LEVEL)


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            cookie_secret=config.COOKIE_SECRET,
            template_path=config.TEMPLATES_ROOT,
            static_path=config.STATIC_ROOT,
            login_url='/login',
            xsrf_cookies=True,
            debug=config.DEBUG,
        )
        super(Application, self).__init__(url_patterns, **settings)


def main():
    # Setting up Tornado application on asyncio
    AsyncIOMainLoop().install()
    app = Application()
    app.listen(config.PORT)

    # Setting up Tornado database
    app.db = peewee_async.PostgresqlDatabase(config.DB_NAME, user=config.DB_USER)
    app.db.set_allow_sync(False)
    app.objects = peewee_async.Manager(app.db)


    # Run loop
    logging.info('Running server on port {}'.format(config.PORT))
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print(" server stopped")


if __name__ == "__main__":
    main()