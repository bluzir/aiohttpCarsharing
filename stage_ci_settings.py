import logging
import os

HOST = '127.0.0.1'
PORT = 9999

DB_NAME = 'twocar_stage'
DB_USER = 'twocar_stage'
DB_PASSWORD = 'CtVWQGlthUqSHdu2fmEA'


# Debug settings
DEBUG = True

if DEBUG:
    LEVEL = logging.DEBUG
else:
    LEVEL = logging.INFO

SECRET_KEY = 'uPoDT+5qRvWni/xLarnefaZ17otdOEPthkc6whvirSo='