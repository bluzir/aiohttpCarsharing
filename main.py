import os

import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket


# websocket example
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
        self.render("index.html")


class WebSocketHandler(tornado.web.RequestHandler):
    pass


def main():
    app = Application()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()