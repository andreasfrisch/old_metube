"""
Django settings for metube project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ldw540jt*s^812brelt8^ap1qkhry2m^g5*7)4ui-qx6*^l!1t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [".metube.dk", "metube.dk"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'metube.project_tracker',
    'metube.fb_crawler',
    'metube.blog',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'metube.urls'

WSGI_APPLICATION = 'metube.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logging
LOGGING = {
	"version": 1,
	"disable_existing_loggers": False,
	# available logging formats
	"formatters": {
		"verbose": {
			"format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
			"datefmt": "%d/%b/%Y %H:%M:%S"
		},
		"simple": {
			"format": "%(levelname)s %(message)s"	
		},

	},
	# "filters": {},
	"handlers": {
		#"default": {
		#	"level": "DEBUG",
		#	"class": "logging.handlers.RotatingFileHandler",
		#	"filename": "default.log",
		#	"formatter": "simple",
		#},
		"file": {
			"level": "DEBUG", # all levels
			"class": "logging.FileHandler",
			"filename": "/tmp/metube.log",
			"formatter": "verbose"

		},	
	},
	"loggers": {
		#"": {
		#	"handlers": ["default"],
		#	"level": "DEBUG",
		#	"propagate": True
		#},
		#"django": {
		#	"handlers": ["file"],
		#	"propagate": True,
		#	"level": "DEBUG",
		#},
		"metube": {
			"handlers": ["file"],
			"level": "DEBUG",
		},
	}
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "../static")
STATICFILES_DIRS = (
	os.path.abspath(os.path.join(BASE_DIR, "metube/static")),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../media"))

TEMPLATE_DIRS = (
	os.path.join(BASE_DIR, "metube/templates"),		
)

# Name of media folder for crawler result files
CRAWLER_RESULTS = "crawler_results"


TINYMCE_DEFAULT_CONFIG = {
	"file_browser_callback": "mce_filebrowser",
}
