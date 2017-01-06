from tornado import gen
from tornado.concurrent import Future
from tornado.httpclient import HTTPClient, AsyncHTTPClient


URL = 'http://bluzir.me'


def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body


def test_callback():
    print('Run callback')


def asynchronous_fetch(url, callback):
    print('Run async fetch')
    http_client = AsyncHTTPClient()

    def handle_response(response):
        callback(response.body)

    http_client.fetch(url, callback=handle_response)


def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result()))
    return my_future


@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    return response.bod



# print(synchronous_fetch(URL))
# print(asynchronous_fetch(URL, test_callback))
# f = async_fetch_future(URL)
f = fetch_coroutine(URL)