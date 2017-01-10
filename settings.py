import peewee_async


# Database settings
DB_NAME = 'test_db'
DB_USER = 'test_user'
DB_PASSWORD = ''

# Database connection
DATABASE = peewee_async.PostgresqlDatabase('test_db', user='test_user')