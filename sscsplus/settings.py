from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-h)5!nydf0^a11!zxvnigy-kl*ilx8n7f35-b4zl)jiu*6zl3dv')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*.onrender.com','.onrender.com','sscsplus.onrender.com','cknews.nav.bd','*.cknews.nav.bd','sscsplus.cknews.nav.bd','sscsplus.pro.bd','sscsplus.nav.bd']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sscsplus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sscsplus.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = 'accounts.CustomUser'

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'bn'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "SSCS+",
    "site_header": "SSCS+",
    "site_brand": "SSCS+ Admin",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Welcome to SSCS+ Administration",
    "copyright": "SSCS+ Finance Management System",
    "search_model": ["accounts.CustomUser", "accounts.Transaction"],
    "topmenu_links": [
        {"name": "Dashboard", "url": "/admin/", "permissions": ["auth.view_user"]},
        {"name": "Front Dashboard", "url": "/dashboard/", "new_window": True},
        {"name": "Fund Transfer", "url": "/ft/", "new_window": True},
        {"name": "Users", "model": "accounts.CustomUser"},
        {"name": "Transactions", "model": "accounts.Transaction"},
    ],
    "usermenu_links": [
        {"name": "View Site", "url": "/dashboard/", "new_window": True, "icon": "fas fa-external-link-alt"},
        {"name": "Support", "url": "mailto:admin@sscs.com", "new_window": True, "icon": "fas fa-envelope"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["accounts", "auth"],
    "custom_links": {
        "accounts": [{
            "name": "Quick Stats",
            "url": "/admin/stats/",
            "icon": "fas fa-chart-pie",
            "permissions": ["accounts.view_transaction"],
        }],
    },
    "icons": {
        "accounts.CustomUser": "fas fa-user-circle",
        "accounts.Transaction": "fas fa-exchange-alt",
        "auth.Group": "fas fa-users-cog",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": "/static/css/style.css",
    "custom_js": "/static/js/script.js",
    "use_google_fonts_cdn": False,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "accounts.CustomUser": "single",
        "accounts.Transaction": "horizontal_tabs",
    },
    "language_chooser": False,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

X_FRAME_OPTIONS = 'SAMEORIGIN'
