import psycopg2

conn = psycopg2.connect(database='test_db',
                        user='test_user',
                        password='qwerty',
                        host='127.0.0.1',
                        port='5433')

cur = conn.cursor()

print(cur)