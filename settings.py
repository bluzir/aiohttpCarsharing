import logging
import os

# Port settings
PORT = 8080

# Folders settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_ROOT = os.path.join(BASE_DIR, 'templates')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
CARS_DATA_FILE = os.path.join(TEMPLATES_ROOT, 'cars_data.json')


# Database settings
DB_NAME = 'test_db'
DB_USER = 'test_user'
DB_PASSWORD = ''


# Debug settings
DEBUG = True

if DEBUG:
    LEVEL = logging.DEBUG
else:
    LEVEL = logging.INFO


# API Keys
GMAPS_API_KEY = 'AIzaSyCZwQePt-z3n2lCnK-nApgzIyxXF3hIMrw'
