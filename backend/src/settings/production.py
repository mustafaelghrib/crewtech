from .development import *

DEBUG = os.environ.get("DJANGO_DEBUG", default=False)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
        'PORT': os.environ.get("POSTGRES_PORT"),
    }
}

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_BUCKET_DOMAIN_NAME = os.environ.get('AWS_BUCKET_DOMAIN_NAME')

STATIC_URL = f'https://{AWS_BUCKET_DOMAIN_NAME}/static/'
STATICFILES_STORAGE = 'src.storage.StaticStorage'

MEDIA_URL = f'https://{AWS_BUCKET_DOMAIN_NAME}/media/'
DEFAULT_FILE_STORAGE = 'src.storage.MediaStorage'
