from .settings import *
import django_heroku

ALLOWED_HOSTS = ['palmfarms.herokuapp.com']
DEBUG = True
IS_DEV = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'palmfarmsDB',
    }
}
# aws
AWS_ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'palmfarms'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'PalmFarms.storage_backends.MediaStorage'

django_heroku.settings(locals())
