import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DEBUG', 1)))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
INTERNAL_IPS = os.getenv('INTERNAL_IPS', '127.0.0.1,localhost').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://127.0.0.1:8090').split(',')
CORS_ORIGIN_WHITELIST = os.getenv('CORS_ORIGIN_WHITELIST', 'http://127.0.0.1:8090').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'channels',
    'core',
    'dynamic_preferences',
    'axes',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'axes.middleware.AxesMiddleware',
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar', ]
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

ROOT_URLCONF = 'AlgorithmManagerProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AlgorithmManagerProject.wsgi.application'

ASGI_APPLICATION = 'AlgorithmManagerProject.asgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("POSTGRES_DB", "postgres_db"),
        'USER': os.getenv("POSTGRES_USER", "postgres_user"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD", "postgres_pass"),
        'HOST': os.getenv("POSTGRES_HOST"),
        'PORT': int(os.getenv("POSTGRES_PORT")),
        'CONN_MAX_AGE': 60 * 10,
    },
}


# Caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv('CACHE_REDIS', "redis://localhost:6379/0"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Authentication backend
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    # 'django_auth_ldap.backend.LDAPBackend',
    'core.backend.AsyncLDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Novosibirsk'
USE_I18N = True
USE_TZ = True

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
static_join = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = static_join

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login settings
LOGIN_URL = '/core/login/'
LOGIN_REDIRECT_URL = '/core/'
LOGOUT_REDIRECT_URL = '/core/login/'

# Celery settings
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/2')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/2')
CELERY_IMPORTS = ("celery_app.tasks",)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Novosibirsk'

# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.getenv('CHANNEL_REDIS_URL', 'redis://127.0.0.1:6379/2')],
        },
    },
}

# Old Logs redis url
LOGS_REDIS_URL = os.getenv('LOGS_REDIS_URL', 'redis://127.0.0.1:6379/2')

MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', 2 * 1024 * 1024 * 1024))  # 2GB

# Axes settings
AXES_FAILURE_LIMIT = 10
AXES_COOLOFF_TIME = timedelta(minutes=30)
AXES_LOCKOUT_PARAMETERS = ["username"]


# Redirect to https connection
SECURE_SSL_REDIRECT = False

# Cookie via only http not javascript
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# transmitted only via https
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# XSS protection
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# settings hsts
SECURE_HSTS_SECONDS = 31536000  # Год
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# time of live sessing and csrf
SESSION_COOKIE_AGE = 604800  # 1 неделя
CSRF_COOKIE_AGE = 15724800  # 6 месяцев


import ldap
from django_auth_ldap.config import LDAPSearch
# LDAP settings
AUTH_LDAP_SERVER_URI = os.getenv('AUTH_LDAP_SERVER_URI', 'ldap://')
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    os.getenv('AUTH_LDAP_BASE_DN', 'ou=People,dc=example,dc=com'),
    ldap.SCOPE_SUBTREE,
    os.getenv('AUTH_LDAP_FILTERSTR', '(uid=%(user)s)'),
)
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}
AUTH_LDAP_ALWAYS_UPDATE_USER = True
