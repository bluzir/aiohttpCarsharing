# Port settings
import logging

PORT = 8080

# Debug settings
DEBUG = True

# Database settings
DB_NAME = 'test_db'
DB_USER = 'test_user'
DB_PASSWORD = ''


# Logging settings
if DEBUG:
    LEVEL = logging.DEBUG
else:
    LEVEL = logging.INFO