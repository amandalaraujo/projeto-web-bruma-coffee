import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- ENVIRON (Configuração de Variáveis de Ambiente) ---
env = environ.Env(
    DEBUG=(bool, False)
)

# Lê o arquivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Variáveis de ambiente com valores padrão de segurança
SECRET_KEY = env('SECRET_KEY', default='django-insecure-teste123')
DEBUG = env('DEBUG', default=True)
NYT_API_KEY = env('NYT_API_KEY', default='teste')

ALLOWED_HOSTS = []

# --- APPLICATION DEFINITION ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.apps.AppConfig',
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# --- DATABASE ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- PASSWORD VALIDATORS ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALIZATION ---

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CONFIGURAÇÕES DE SESSÃO (Segurança do Usuário) ---
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Encerra a sessão ao fechar o navegador
SESSION_COOKIE_AGE = 3600               # 1 hora de inatividade
SESSION_SAVE_EVERY_REQUEST = True

# --- STATIC FILES (CSS, JavaScript, Images) ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# --- MEDIA FILES (Upload de Fotos de Perfil) ---
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

COTTON_DIR = 'components'