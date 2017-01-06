import momoko
from tornado.ioloop import IOLoop
ioloop = IOLoop.instance()

conn = momoko.Connection("dbname=test_db user=test_user port=5433")
future = conn.connect()

ioloop.add_future(future, lambda x: ioloop.stop())
ioloop.start()
future.result()  # raises exception on connection error

future = conn.execute("SELECT * FROM users")
ioloop.add_future(future, lambda x: ioloop.stop())
ioloop.start()
cursor = future.result()
rows = cursor.fetchall()

print(rows)