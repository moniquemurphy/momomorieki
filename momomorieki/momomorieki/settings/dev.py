from .base import *

DEBUG = True
SECRET_KEY = '(*ycu=ro*228n4en2yl2h5=fp3!t90ms)ek-$=#sf=nmcyv6ah'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'momomorieki',
        'USER': 'django',
        'PASSWORD': os.environ['MOMOMORIEKI_PASSWORD'],
        'HOST': 'localhost',
        'PORT': 5432,
    }
}