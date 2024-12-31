from .base import *

import environ

env = environ.Env()
environ.Env.read_env()

DEBUG = False

ALLOWED_HOSTS = ["skycars.ovh", "www.skycars.ovh", "dev.skycars.ovh", env('SERVER_IP')]
CORS_ALLOWED_ORIGINS = [
    "http://www.skycars.ovh",
    "https://www.skycars.ovh",
    "http://dev.skycars.ovh",
    "https://dev.skycars.ovh",
]
CSRF_TRUSTED_ORIGINS=['https://*.skycars.ovh'] 

SECRET_KEY = env('SECRET_KEY')

###### DB CONFIG ######
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env.int('DB_PORT'),
        "ATOMIC_REQUESTS": True,
    }
}

###### SMTP CONFIG ######
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

###### AWS CONFIG ######
FILES_FOLDER = env("FILES_FOLDER")
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": env("AWS_ACCESS_KEY_ID"),
            "secret_key": env("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": env("AWS_STORAGE_BUCKET_NAME"),
            "region_name": env("AWS_S3_REGION_NAME"),
            "default_acl": env("AWS_DEFAULT_ACL"),
            "querystring_auth": env("AWS_QUERYSTRING_AUTH"),
            "querystring_expire": env("AWS_QUERYSTRING_EXPIRE")
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": env("AWS_ACCESS_KEY_ID"),
            "secret_key": env("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": env("AWS_STORAGE_BUCKET_NAME"),
            "region_name": env("AWS_S3_REGION_NAME"),
        },
    }
}

###### LOG CONFIG ######
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/erros.log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 5, 
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'skyCarManager': {
            'handlers': ['file', 'console'],
            'level': 'ERROR', 
            'propagate': False,
        },
    },
}
