import os
import mimetypes
from .settings_base import *

'''
This file is used to create a local settings_local.py file for development
'''



DEBUG = True

ADMIN_GROUP = 'admins'
USERS_GROUP = 'users'

PAGINATE_BY = 10

ALLOWED_ORIGINS = ['127.0.0.1']


DJANGO_DEVELOPMENT = True


mimetypes.add_type("text/css", ".css", True)


if DJANGO_DEVELOPMENT:
    # In development, use the Webpack dev server
    WEBPACK_DEV_SERVER = 'http://localhost:9000/static/dist/'
    STATICFILES_DIRS = [
        BASE_DIR / "static/dist",
    ]
else:
    # In production, use the collected static files
    #print(os.getenv('DJANGO_DEVELOPMENT'))
    STATIC_ROOT = BASE_DIR / "staticfiles"
    WEBPACK_DEV_SERVER = STATIC_URL + 'dist/'

CORS_ORIGIN_WHITELIST = [
     'http://localhost:3000'
]

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
INTERNAL_IPS = ('127.0.0.1', '0.0.0.0')


INSTALLED_APPS += (
    'corsheaders',
    'debug_toolbar',
    'django_extensions',
)

GOOGLE_MAPS_API_KEY = ''

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel'
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    'EXTRA_SIGNALS': [],
}

TEMPLATES[0]['OPTIONS']['loaders'] = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For postgres with postgis

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': '',
#         'USER': 'postgres',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '5432',
#         'CONN_MAX_AGE': 60 * 10
#     }
# }


# For postgres with postgres

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': '',
#         'USER': 'postgres',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '5432',
#         'CONN_MAX_AGE': 60 * 10
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


AUTH_PASSWORD_VALIDATORS = []
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = "default"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


try:
     # configure based on your env configuration
    if os.name == 'nt':
        os.environ['PATH'] = os.path.join(VIRTUAL_ENV_DIR, r'.\Lib\site-packages\osgeo') + ';' + os.environ['PATH']
        os.environ['PROJ_LIB'] = os.path.join(VIRTUAL_ENV_DIR, r'.\Lib\site-packages\osgeo\data\proj') + ';' + os.environ['PATH']
        GDAL_LIBRARY_PATH = os.path.join(VIRTUAL_ENV_DIR, r'.\Lib\site-packages\osgeo\gdal.dll')
        GEOS_LIBRARY_PATH = os.path.join(VIRTUAL_ENV_DIR, r'.\Lib\site-packages\osgeo\geos_c.dll')
except:
    pass



