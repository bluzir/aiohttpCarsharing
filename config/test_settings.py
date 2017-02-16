import logging
import os


# SSL Settings
CRT_ROOT = '/etc/letsencrypt/live/bluzir.me/fullchain.pem'
KEY_ROOT = '/etc/letsencrypt/live/bluzir.me/privkey.pem'

# Host settings
HOST = '89.223.26.255'
PORT = 8080


# Database settings
DB_NAME = 'test_db'
DB_USER = 'test_user'
DB_PASSWORD = ''

# Secret key settings
SECRET_KEY = 'uPoDT+5qRvWni/xLarnefaZ17otdOEPthkc6whvirSo='


# Debug settings
DEBUG = True

if DEBUG:
    LEVEL = logging.DEBUG
else:
    LEVEL = logging.INFO


# API Keys
GMAPS_API_KEY = 'AIzaSyCZwQePt-z3n2lCnK-nApgzIyxXF3hIMrw'
INPLAT_API_KEY = 'EVrAuGGEjgN020MmMdwV0dqp'
