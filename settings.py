import logging
import os



PORT = 8080

# Auth settings
COOKIE_SECRET = 'kzWkZTHsR5WCTGqYAlWSeWK0rDOfG0+ktIJnUSMyFOA='

# Folders settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_ROOT = os.path.join(BASE_DIR, 'templates')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Debug settings
DEBUG = True

# Database settings
DB_NAME = 'test_db'
DB_USER = 'test_user'
DB_PASSWORD = ''


# Logging settings
if DEBUG:
    LEVEL = logging.DEBUG
    AUTORELOAD = True
    TRACEBACK = True
else:
    LEVEL = logging.INFO
    AUTORELOAD = False
    TARCEBACK = False