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
from settings import DATABASE

logging.basicConfig(level=logging.DEBUG)
storage = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
PORT = 8080



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/websocket", WebSocketHandler),
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
        self.render("index.html", messages=WebSocketHandler.cache)


class RegistrationHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("registration.html")



# websocket example
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache_size = 200
    cache = storage.get('messages')
    cache = ast.literal_eval(cache)  # FIX
    if not cache:
        cache = []

    def open(self):
        logging.info("Opened websocket")
        WebSocketHandler.waiters.add(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]
        storage.set('messages', cls.cache)

    @classmethod
    def send_updates(cls, chat):
        logging.info("Sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("Message: {}".format(message))
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"],
            }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))

        WebSocketHandler.update_cache(chat)
        WebSocketHandler.send_updates(chat)

    def on_close(self):
        logging.info("Websocket closed")
        WebSocketHandler.waiters.remove(self)

    def check_origin(self, origin):
        return True


def main():
    app = Application()
    app.listen(PORT)
    app.objects = peewee_async.Manager(DATABASE)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    logging.info('Running server on port {}'.format(PORT))
    main()
