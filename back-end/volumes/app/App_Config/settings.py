from pathlib import Path
from datetime import timedelta
from decouple import config
from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['*', 'app']
CSRF_TRUSTED_ORIGINS = ['http://localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',   
    
    # Apps
    'Extentions',
    'app_auth.apps.AppAuthConfig',
    'app_api.apps.AppApiConfig',

    # Packs
    'rest_framework',
    'corsheaders',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',           # add for translating
    "corsheaders.middleware.CorsMiddleware",               # add for cors origin
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'App_Config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = config('WSGI_APPLICATION')


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
]
LANGUAGE_CODE = config('LANGUAGE_CODE')
TIME_ZONE = config('TIME_ZONE')
USE_I18N = config('USE_I18N')
USE_TZ = config('USE_TZ')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'static_files'
STATICFILES_DIRS = [ Path("assets") ]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'media_files'


# ######### Custom User ######### #
AUTH_USER_MODEL = config('AUTH_USER_MODEL')

# ######### API ######### #
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8080',
] 

# ######### SIMPLE JWT ######### #
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7)
}

# ######### DRF ######### #
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
#     'DEFAULT_PARSER_CLASSES': (
#         # 'rest_framework.parsers.JSONParser',
#         'rest_framework.parsers.FormParser',
#         'rest_framework.parsers.MultiPartParser',
#     ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}
