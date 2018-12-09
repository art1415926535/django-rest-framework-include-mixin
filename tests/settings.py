DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = '42'

ROOT_URLCONF = 'tests.urls'

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',

    'tests',
]
