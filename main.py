import ast
import logging
import os
import uuid

import peewee_async
import redis
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

from models import Users

logging.basicConfig(level=logging.DEBUG)
storage = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
PORT = 8080



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


def main():
    app = Application()
    app.listen(PORT)
    app.objects = peewee_async.Manager(DATABASE)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    logging.info('Running server on port {}'.format(PORT))
    main()
