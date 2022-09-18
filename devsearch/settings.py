from decouple import config
from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = [os.environ.get('SECRET_KEY'), config('SECRET_KEY')]


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if os.getcwd() == '/app':
    DEBUG = False

ALLOWED_HOSTS = ['https://devworlddd.herokuapp.com/', 'devworlddd.herokuapp.com', 'www.devworlddd.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'projects.apps.ProjectsConfig',
    'users.apps.UsersConfig',

    'rest_framework',
]

# I GET AN ERROR WHEN I USE djangorestframework-simplejwt WHEN I USE POSTMAN
# WHEN I PASS IN A CORRECT USERNAME AND PASSWORD IN BODY-RAW-JSON
# I GET A TYPE ERROR "Expected a string value" 

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ]
# }


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    "whitenoise.middleware.WhiteNoiseMiddleware",

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'devsearch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # look in for a folder named 'templates' in the base directory
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'devsearch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


try:
    EMAIL_BACKEND= config('EMAIL_BACKEND')
    EMAIL_HOST_PASSWORD= config('EMAIL_HOST_PASSWORD')
    EMAIL_HOST_USER= config('EMAIL_HOST_USER')
    EMAIL_HOST= config('EMAIL_HOST')
    EMAIL_PORT= config('EMAIL_PORT')
    EMAIL_USE_TLS= config('EMAIL_USE_TLS')
except:
    EMAIL_BACKEND= os.environ.get('EMAIL_BACKEND')
    EMAIL_HOST_PASSWORD= os.environ.get('EMAIL_HOST_PASSWORD')
    EMAIL_HOST_USER= os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST= os.environ.get('EMAIL_HOST')
    EMAIL_PORT= os.environ.get('EMAIL_PORT')
    EMAIL_USE_TLS= os.environ.get('EMAIL_USE_TLS')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
# TELLS DJANGO THAT THE MEDIA IS INSIDE STATIC/IMAGES/
MEDIA_URL = '/images/'

# TELL THE SYSTEM TO LOOK FOR A FOLDER NAMED 'static' AND USE THAT AS THE DIRECTORY FOR STATICFILES.
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static')
    # newer version of django
    BASE_DIR / 'static'
]

#  TELLS DJANGO WHERE TO SAVE UPLOADED MEDIA CONTENTS
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
# DEFINES WHERE OUR STATIC FILES IN PRODUCTION ARE
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if os.getcwd() == '/app':
    DEBUG = False