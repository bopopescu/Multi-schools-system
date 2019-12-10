import os
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import constants as message_constants
MESSAGE_LEVEL = message_constants.DEBUG

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'twq$^$5g%j7=k06fglkifr@r)g8an#kx&!v*3a=_t#2d0r3ogd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['localhost', '.localhost']

ALLOWED_HOSTS = []

# # Application definition
# # Application definition
# SHARED_APPS = (
#     'tenant_schemas',  # mandatory, should always be before any django app
#     'schools',  # you must list the app where your tenant model resides in
#
#     'django.contrib.contenttypes',
#
#     # everything below here is optional
#     'django.contrib.auth',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.admin',
#     'django.contrib.staticfiles',
# )
#
# TENANT_APPS = (
#     'django.contrib.contenttypes',
#     'django.contrib.auth',
#
#     # your tenant-specific apps
#     'schools',
#     )
#
# TENANT_MODEL = "schools.Holder"

INSTALLED_APPS = [
    # 'tenant_schemas',  # mandatory, should always be before any django app

    'schools.apps.SchoolsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'widget_tweaks',
    'crispy_forms',
    # 'tinymce',

    'sorl.thumbnail',
    'allauth',

    'graphene_django',
    'markdownx',
    'taggit',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'import_export',
    'twilio',
    'reportlab',
    'xhtml2pdf',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

BOOTSTRAP4 = {
    'include_jquery': True,
}

MIDDLEWARE = [
    #   'Education.middleware.TenantTutorialMiddleware',
    #   'tenant_schemas.middleware.TenantMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Education.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'Education.urls'
#
# PUBLIC_SCHEMA_URLCONF = 'Education.urls_public'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'Education.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'tenant_schemas.postgresql_backend',
#         'NAME': 'schools',
#         'USER': 'postgres',
#         'PASSWORD': 'pass12345',
#         'HOST': 'localhost'
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASE_ROUTERS = (
#     'tenant_schemas.routers.TenantSyncRouter',
# )


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
LANGUAGES = (
            ('en', 'English'),
            ('de', 'German'),
            ('bg', 'Bulgarian'),
            ('es', 'Spanish'),
            ('ru', 'Russian'),
            ('nl', 'Dutch'),
            ('pt', 'Portuguese'),
            ('el', 'Greek'),
            ('cs', 'Czech'),
            ('sv', 'Swedish'),
            ('no', 'Norwegian'),
            ('fr', 'French'),
)

# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Kampala'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

AUTH_USER_MODEL = 'schools.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/canon/dashboard/'
LOGOUT_REDIRECT_URL = '/canon/auth/login/'
LOGIN_URL = '/canon/auth/login/'

LOGIN_EXEMPT_URLS = (
    # 'canon/',
    'canon/auth/logout/',
    'canon/profile/password/reset/',
    'canon/profile/password/reset/done/',
    'canon/profile/password-reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/',
    'canon/profile/reset/password/complete/',
)

IMPORT_EXPORT_USE_TRANSACTIONS = True

# SESSION_EXPIRE_SECONDS = 1200  # 1200 seconds = 10 minutes
# SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
# SESSION_COOKIE_AGE = 60 * 10  # Session will expiry after 10 minutes idle.
# SESSION_SAVE_EVERY_REQUEST = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')

TEMPLATES[0]['OPTIONS']['context_processors'].append("schools.context_processors.term_processor")
TEMPLATES[0]['OPTIONS']['context_processors'].append("schools.context_processors.year_processor")

# DEFAULT_FILE_STORAGE = 'tenant_schemas.storage.TenantFileSystemStorage'
