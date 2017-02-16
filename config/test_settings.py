import logging
import os


# SSL Settings
CRT_ROOT = '/etc/letsencrypt/live/bluzir.me/fullchain.pem'
KEY_ROOT = '/etc/letsencrypt/live/bluzir.me/privkey.pem'

# Host settings
HOST = '127.0.0.1'
PORT = 9090


# Database settings
DB_NAME = 'twocar_stage'
DB_USER = 'twocar_stage'
DB_PASSWORD = 'CtVWQGlthUqSHdu2fmEA'

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
