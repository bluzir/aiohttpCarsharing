import logging


# websocket example
import tornado as tornado


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/websocket", WebSocketHandler),
        ]


class MainHandler:
    pass


class WebSocketHandler:
    pass


def main():
    app = Application()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()