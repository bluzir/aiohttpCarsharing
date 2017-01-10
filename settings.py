import peewee_async

# Debug settings
DEBUG = True

# Database settings
DB_NAME = 'test_db'
DB_USER = 'test_user'
DB_PASSWORD = ''


# Database connection
def main():
    DATABASE = peewee_async.PostgresqlDatabase(DB_NAME, user=DB_USER)


if __name__ == '__main__':
    main()