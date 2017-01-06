import logging

import psycopg2


conn = psycopg2.connect("dbname=test_db user=test_user port=5433")
cur = conn.cursor()
cur.execute('SELECT * FROM users;')
q = cur.fetchone()



print(q)