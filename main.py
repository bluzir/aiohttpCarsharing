import logging
import os
import uuid

import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

logging.basicConfig(level=logging.INFO)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/websocket", WebSocketHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=WebSocketHandler.cache)


# websocket example
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    cache = []

    def open(self):
        logging.info("Opened websocket")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        logging.info("Websocket closed")

    def check_origin(self, origin):
        return True


def main():
    app = Application()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
