import logging
import os

HOST = '127.0.0.1'
PORT = 9090

# Database settings
DB_NAME = 'twocar_stage'
DB_USER = 'postgres'
DB_PASSWORD = ''


# Debug settings
DEBUG = True

if DEBUG:
    LEVEL = logging.DEBUG
else:
    LEVEL = logging.INFO
