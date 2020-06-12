import os

try:
    from . import conf
except ImportError:
    print("conf.py not found")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SECRET_KEY = conf.SECRET_KEY

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.core.apps.CoreConfig',
    'apps.users.apps.UsersConfig',
    'apps.restapi.apps.RestapiConfig',

    'social_django',
    'rest_framework',
    'corsheaders',
    'captcha',
    'djcelery_email',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tatartwin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'tatartwin.wsgi.application'


AUTHENTICATION_BACKENDS = {
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
}
LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', 'Russian'),
)
LOCALE_PATHS = (
    'locale',
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SOCIAL_AUTH_VK_OAUTH2_KEY = conf.SOCIAL_AUTH_VK_OAUTH2_KEY
SOCIAL_AUTH_VK_OAUTH2_SECRET = conf.SOCIAL_AUTH_VK_OAUTH2_SECRET

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

EMAIL_HOST = conf.EMAIL_HOST
EMAIL_HOST_USER = conf.EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = conf.DEFAULT_FROM_EMAIL
EMAIL_HOST_PASSWORD = conf.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = conf.EMAIL_USE_TLS
EMAIL_PORT = conf.EMAIL_PORT
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

AUTH_USER_MODEL = 'users.TatarUser'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'sessions': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': conf.NAME,
        'USER': conf.USER,
        'PASSWORD': conf.PASSWORD,
        'HOST': conf.HOST,
        'PORT': conf.PORT,
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "sessions"

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'