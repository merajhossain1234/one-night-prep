

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-27uie(96pk2435s%d$7+%u3mu8elp3aq7ma$!g4j_ye)&in$)p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom apps
    'accounts',
    'ai',
    'session',
    
    # installed third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # This is correct
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",  # This is valid
]

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'EMAIL_AUTHENTICATION': True,
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }

}

SITE_ID = 1

ROOT_URLCONF = 'onenightprep.urls'

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


AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
]


# AUTHENTICATION_BACKENDS = (
#     "django.contrib.auth.backends.ModelBackend",
#     "allauth.account.auth_backends.AuthenticationBackend",
# )




WSGI_APPLICATION = 'onenightprep.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'onenightprep',  # Change this to your database name
        'USER': 'Admin',  # Change this to your database user
        'PASSWORD': '30xy75t',  # Change this to your database password
        'HOST': 'db',  # This should match the service name in your docker-compose file
        'PORT': '5432',  # Default PostgreSQL port
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'accounts.User'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / "frontend/assets",  # Ensure this path is correct
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# EMAIL_BACKEND = 'django_ses.SESBackend'
# EMAIL_FILE_PATH = BASE_DIR/'tmp/email'
# EMAIL_HOST_USER = "admin@weordr.com"


# DEFAULT_FROM_EMAIL = 'admin@weordr.com'