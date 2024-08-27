"""
Django settings for blackpearl_web_py project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g7l6@87%$@@rww4rh%r5)9&#t4j%weelou1)$^h^#$abp5!5f!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'blackpearl_admin',
    'blackpearl_frntend',
]

JAZZMIN_SETTINGS = {
    "site_title":"BlackPearl admin",
    "site_header": "Black Pearl",
    "site_brand": "Black Pearl",
    # "site_logo": "/user/images/favicon.png",
    "welcome_sign": "Welcome to Black Pearl",
    "copyright": "hibacbv@gmail.com",
    "show_ui_builder": False,
    "icons": {
        "auth": "fas fa-users-cog",
        
        "blackpearl_admin.user": "fas fa-user",
        "blackpearl_admin.Villa": "fas fa-hotel",
        "blackpearl_admin.DestinationLocations": "fas fa-location-arrow",
        "blackpearl_admin.Offers":"fas fa-percent",
        "blackpearl_admin.Coupon_code":"fas fa-money-bill-wave",
        "blackpearl_admin.PartnerWithUs":"fas fa-hands-helping",
        "blackpearl_admin.Subscription":"fas fa-subscript",
        "blackpearl_admin.FAQ":"fas fa-question",
        "blackpearl_admin.ContactUs":"fas fa-address-book",
        "blackpearl_admin.Booking":"fas fa-store-alt",
        
        "blackpearl_admin.Blog":"fab fa-blogger",
        
        "blackpearl_admin.Aminities":"fas fa-concierge-bell",
        "blackpearl_admin.Brand":"fas fa-ad",
        "blackpearl_admin.Testimonial":"fas fa-smile",
        "blackpearl_admin.GSTValues":"fas fa-money-bill",
        "blackpearl_admin.MasterData":"fas fa-user-cog",
        "blackpearl_admin.SCOMeta":"fas fa-sitemap",
        
        "auth.Group": "fas fa-users",
        
        "taggit.Tag":"fas fa-tag"
    },
    # "usermenu_links": [
    #     {"name": _("Database Backup"), 
    #      "url": "http://127.0.0.1:8000/db-backup", 
    #      "new_window": True,
    #      "icon":"fas fa-database",
    #     }
    # ],
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blackpearl_web_py.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'blackpearl_web_py.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# authuser
# AUTH_USER_MODEL = 'blackpearl_frntend.CustomerUser'

# AUTHENTICATION_BACKENDS = [
#     'blackpearl_frntend.custom_authentication.EmailBackend',  # Ensure correct path
#     'django.contrib.auth.backends.ModelBackend',  # Default backend
# ]


from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

#ckeditor config
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': '100%',
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_COOKIE_SECURE = False  # Set to True if using HTTPS
CSRF_COOKIE_HTTPONLY = False

