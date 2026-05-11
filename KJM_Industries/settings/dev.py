"""
Development settings for KJM_Industries.

Usage:
    DJANGO_SETTINGS_MODULE=KJM_Industries.settings.dev

Docs: https://docs.djangoproject.com/en/stable/topics/settings/
"""

from .base import *  # noqa: F403

# -----------------------------------------------------------------------------
# CORE
# -----------------------------------------------------------------------------

# Defaults to True in dev
DEBUG = os.getenv("DEBUG", "True") == "True"  # noqa: F405

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

# Required for Django Debug Toolbar to render.
INTERNAL_IPS = [
    "127.0.0.1",
]

# Required when running the dev server behind a tunnel (e.g. Cloudflare Tunnel)
# or accessing from a non-localhost origin during development.
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")  # noqa: F405

# -----------------------------------------------------------------------------
# SECURITY OVERRIDES
# Disabling production security settings that break local HTTP development.
# Docs: https://docs.djangoproject.com/en/stable/topics/security/
# -----------------------------------------------------------------------------

SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# -----------------------------------------------------------------------------
# APPLICATIONS
# -----------------------------------------------------------------------------

INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
    "django_browser_reload",
    "django_watchfiles",
]

# -----------------------------------------------------------------------------
# MIDDLEWARE
# Inserted by name relative to SecurityMiddleware so position stays correct
# regardless of any reordering in base.py.
# Docs: https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
# -----------------------------------------------------------------------------

MIDDLEWARE.insert(  # noqa: F405
    MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1,  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)
MIDDLEWARE.insert(  # noqa: F405
    MIDDLEWARE.index("debug_toolbar.middleware.DebugToolbarMiddleware") + 1,  # noqa: F405
    "django_browser_reload.middleware.BrowserReloadMiddleware",
)

# -----------------------------------------------------------------------------
# DATABASE
# Uses a separate Neon branch or database for development.
# ssl_require=True is intentional — Neon requires SSL on all connections
# regardless of environment.
# Docs: https://neon.tech/docs/connect/connect-from-any-app
# -----------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------------------------------------------------------
# EMAIL
# Prints emails to the console instead of sending them.
# Swap for a real backend (e.g. Mailpit) if you need to test HTML email rendering.
# Docs: https://docs.djangoproject.com/en/stable/topics/email/#console-backend
# -----------------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"