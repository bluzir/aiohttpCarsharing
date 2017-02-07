from config.local_settings import *

# Folders settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_ROOT = os.path.join(BASE_DIR, 'templates')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

