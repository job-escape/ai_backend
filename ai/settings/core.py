import os
import json
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, "ai/.env"))

SECRET_KEY = env("DJANGO_SECRET")
DEBUG = env("DEBUG", "true").lower() == "true"
STAGE = not (env("STAGE", "true").lower() == "true" and env("DATABASE_SELECTOR") == "prod")

if STAGE:
    stage_generate_tasks_json = env("STAGE_GENERATE_TASKS")
    stage_jwt_secrets_json = env("STAGE_JWT_SECRETS")
    ai_stage_db_json = env("AI_STAGE_DB")
else:
    ai_prod_db_json = env("AI_PROD_DB")
    prod_generate_tasks_json = env("PROD_GENERATE_TASKS")
    prod_jwt_secrets_json = env("PROD_JWT_SECRETS")

aws_secrets_json = env("AWS_SECRETS")
general_ai_tools_json = env("GENERAL_AI_TOOLS")
gpt_secrets_json = env("GPT_SECRETS")
gcp_infos_json = env("GCP_INFOS")

# Parse the JSON strings into dictionaries, if they exist
ai_stage_db = json.loads(ai_stage_db_json) if ai_stage_db_json else {}
ai_prod_db = json.loads(ai_prod_db_json) if ai_prod_db_json else {}
aws_secrets = json.loads(aws_secrets_json) if aws_secrets_json else {}
stage_generate_tasks = json.loads(stage_generate_tasks_json) if stage_generate_tasks_json else {}
prod_generate_tasks = json.loads(prod_generate_tasks_json) if prod_generate_tasks_json else {}
general_ai_tools = json.loads(general_ai_tools_json) if general_ai_tools_json else {}
gpt_secrets = json.loads(gpt_secrets_json) if gpt_secrets_json else {}
gcp_infos = json.loads(gcp_infos_json) if gcp_infos_json else {}
stage_jwt_secrets = json.loads(stage_jwt_secrets_json) if stage_jwt_secrets_json else {}
prod_jwt_secrets = json.loads(prod_jwt_secrets_json) if prod_jwt_secrets_json else {}


# HOSTS
ALLOWED_HOSTS = ['api.jobescape.me', 'api.jobescape.us', 'localhost']
if STAGE:
    ALLOWED_HOSTS = [
        'stage.api.jobescape.me', 
        'stage.api.jobescape.us', 
        'ai-stage-397596874269.us-east1.run.app'
    ]
if DEBUG:
    ALLOWED_HOSTS.extend([
        '.localhost', 
        '127.0.0.1', 
        '[::1]', 
        '0.0.0.0', 
        # env("NGROK_HOST", str)
        ])
    # NGROK_IP = env("NGROK_IP", str)
    # CSRF_TRUSTED_ORIGINS = [NGROK_IP]


# CORS
CORS_ALLOWED_ORIGINS = [
    "https://jobescape.me",  # new funnel
    "https://api.jobescape.me",  # backend
    "https://app.jobescape.me",  # new app
    "https://jobescape.us",  # new app
    "https://app.jobescape.us",
    "https://analytics.jobescape.me",
]
if STAGE:
    CORS_ALLOWED_ORIGINS.extend([
        "https://stage.jobescape.me",  # stage app
        "https://funnels.jobescape.me",  # stage funnel
        "https://funnels.jobescape.us",  # stage funnel
    ])
if DEBUG:
    CORS_ALLOWED_ORIGINS.extend([
        "http://0.0.0.0:80",
        "http://172.31.19.3",
        "https://stage3.jobescape.me",
        # env("LOCAL_IP", str),
        # env("NGROK_IP", str)
        ]
    )
    CORS_ALLOWED_ORIGIN_REGEXES = [
        # r"^https:\/\/.+\.ngrok-free\.app$",
        r"^http:\/\/localhost(:[0-9]*)?$",
        r"^https:\/\/.+jobescape-team\.vercel\.app"
    ]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'chat',
    'interview_prep',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
]
if DEBUG:
    INSTALLED_APPS.append('silk')

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

if DEBUG:
    MIDDLEWARE.append('silk.middleware.SilkyMiddleware')

ROOT_URLCONF = 'ai.urls'

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

WSGI_APPLICATION = 'ai.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'dev': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ai_stage_db.get('DEVELOPMENT_DB_NAME', ""),
        'USER': ai_stage_db.get('DEVELOPMENT_DB_USER', ""),
        'PASSWORD': ai_stage_db.get('DEVELOPMENT_DB_PASS', ""),
        'HOST': ai_stage_db.get('DEVELOPMENT_DB_HOST', ""),
        'PORT': ai_stage_db.get('DEVELOPMENT_DB_PORT', ""),
    },
    'prod': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ai_prod_db.get('PRODUCTION_DB_NAME', ""),
        'USER': ai_prod_db.get('PRODUCTION_DB_USER', ""),
        'PASSWORD': ai_prod_db.get('PRODUCTION_DB_PASS', ""),
        'HOST': ai_prod_db.get('PRODUCTION_DB_HOST', ""),
        'PORT': ai_prod_db.get('PRODUCTION_DB_PORT', ""),
        'DISABLE_SERVER_SIDE_CURSORS': True,
    },
}
DATABASE_SELECTOR = env("DATABASE_SELECTOR", "dev")
DATABASES["default"].update(DATABASES[env("DATABASE_SELECTOR")])

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': ('custom.custom_backend.PrefetchedJWTAuthentication',),
}

SIMPLE_JWT = {
    'SIGNING_KEY': stage_jwt_secrets.get("JWT_SIGNING_KEY") if STAGE else prod_jwt_secrets.get("JWT_SIGNING_KEY"),
    'ALGORITHM': stage_jwt_secrets.get("JWT_ALGORITHM") if STAGE else stage_jwt_secrets.get("JWT_ALGORITHM")
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
AWS_ACCESS_KEY_ID = aws_secrets.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = aws_secrets.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = aws_secrets.get('AWS_STORAGE_BUCKET_NAME')
AWS_CLOUDFRONT_DOMAIN = aws_secrets.get('AWS_CLOUDFRONT_DOMAIN')
AWS_S3_CUSTOM_DOMAIN = aws_secrets.get('AWS_S3_CUSTOM_DOMAIN')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
if AWS_ACCESS_KEY_ID:
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'
    MEDIAFILES_LOCATION = 'media'
    MEDIA_ROOT = '/%s/' % MEDIAFILES_LOCATION
    MEDIA_URL = '//%s/%s/' % (AWS_CLOUDFRONT_DOMAIN, MEDIAFILES_LOCATION)
    DEFAULT_FILE_STORAGE = 'custom.custom_storage.MediaStorage'

    STATICFILES_LOCATION = 'static'
    STATIC_ROOT = '/%s/' % STATICFILES_LOCATION
    # STATIC_URL = '//%s/%s/' % (AWS_CLOUDFRONT_DOMAIN, STATICFILES_LOCATION)
    STATIC_URL = 'https://%s/%s/' % (AWS_CLOUDFRONT_DOMAIN, STATICFILES_LOCATION)
    STATICFILES_STORAGE = 'custom.custom_storage.StaticStorage'
