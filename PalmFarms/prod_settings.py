from .settings import *
import django_heroku

ALLOWED_HOSTS = ['palmfarms.herokuapp.com']
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'palmfarmsDB',
    }
}

django_heroku.settings(locals())
