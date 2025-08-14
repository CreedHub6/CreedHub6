from pathlib import Path
import os
import environ

# ---------------------------------------------------------------------
# Base directory
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------
# Load environment variables from .env.local
# ---------------------------------------------------------------------
env = environ.Env()
env_file = os.path.join(BASE_DIR, '.env.local')
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

# ---------------------------------------------------------------------
# Security settings
# ---------------------------------------------------------------------
SECRET_KEY = env(
    'SECRET_KEY',
    default='django-insecure-$1dw+3=6$q6=(57l_a^!%8d9-+h^__w7+zvpwv$d_^ocz8x+cl'
)
DEBUG = False
ALLOWED_HOSTS = ['creedhub6.onrender.com']

# ---------------------------------------------------------------------
# Installed apps
# ---------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Cloudinary for media storage
    'cloudinary',
    'cloudinary_storage',

    # Local apps
    'systemapp',
]

# ---------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static file serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------------------------------------------------
# URL configuration & Templates
# ---------------------------------------------------------------------
ROOT_URLCONF = 'onlinefoodorderingsystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'onlinefoodorderingsystem.wsgi.application'

# ---------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------
# Static files (CSS, JS)
# ---------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------------------------------------------------------------
# Media storage (Cloudinary)
# ---------------------------------------------------------------------
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
}

# ---------------------------------------------------------------------
# Default primary key field type
# ---------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------
# Authentication redirects
# ---------------------------------------------------------------------
LOGIN_URL = 'user_login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/user_login/'

# ---------------------------------------------------------------------
# Paystack
# ---------------------------------------------------------------------
PAYSTACK_SECRET_KEY = env(
    'PAYSTACK_SECRET_KEY',
    default='sk_test_8d90ea3ebcd9b6b925625d10b0230ea3df764975'
)
