"""
Django settings for syc project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qo(7!b5!0pzlclajpjh&5)+3p_=w6zuk#g$c@5=l7+w#zdt1(4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'storage.apps.StorageConfig',
    'customer.apps.CustomerConfig',
    'plan.apps.PlanConfig',
    'purchase.apps.PurchaseConfig',
    'report.apps.ReportConfig',
    'user.apps.UserConfig',
    'system.apps.SystemConfig',
    'information.apps.InformationConfig',

    # 工资统计
    'salary.apps.SalaryConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # my_middleware
    'common.my_middleware.SignInCheck'
]

ROOT_URLCONF = 'syc.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'syc.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'syc',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': 3306
    },

    'salary': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'syc_salary',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': 3306
    }
}

DATABASE_ROUTERS = ['syc.database_router.MyRouter']


DATABASE_APPS_MAPPING = {
    'salary': 'salary',
    'customer': 'default',
    'information': 'default',
    'plan': 'default',
    'purchase': 'default',
    'report': 'default',
    'storage': 'default',
    'system': 'default',
    'user': 'default'
}

# Redis Config
REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 4
}

# 使用 Redis 作为缓存后端
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1,
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

FILE_BAK = os.path.join(BASE_DIR, 'file_bak')
PURCHASE_BAK = os.path.join(BASE_DIR, 'file_bak' + os.sep + 'purchase')
PLAN_BAK = os.path.join(BASE_DIR, 'file_bak' + os.sep + 'plan')
STORAGE_BAK = os.path.join(BASE_DIR, 'file_bak' + os.sep + 'storage')
CUSTOMER_BAK = os.path.join(BASE_DIR, 'file_bak' + os.sep + 'customer')
PURCHASE_OUTPUT = os.path.join(BASE_DIR, 'file_bak' + os.sep + 'purchase_output')
PURCHASE_TRANSLATION_ORIGIN = os.path.join(BASE_DIR, 'file_bak' + os.sep + 'purchase_translation')
STORAGE_IN = os.path.join(BASE_DIR, 'file_bak' + os.sep + 'storage_in')
FINISHSTATEMENTOUT = os.path.join(BASE_DIR, 'file_bak' + os.sep + 'statement' + os.sep + 'finish')
PURCHASESTATEMENTOUT = os.path.join(BASE_DIR, 'file_bak' + os.sep + 'statement' + os.sep + 'purchase')
