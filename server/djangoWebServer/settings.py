import datetime
import os
from datetime import timedelta
from pathlib import Path

from cryptography.fernet import Fernet

BASE_DIR = Path(__file__).resolve().parent.parent

# 配置静态网页的代理
STATIC_URL = '/static/'


SECRET_KEY = 'django-insecure-ypu2=#s5wqperumf6kmmi=eb4)u=#sror+nsa*kq$dfkhm7-a-'

# token对称加密秘钥
# 秘钥，用于加密和解密前端的 Token
token_SECRET_KEY = b'lgYdcCA1tc5odYAkri_fYg2UuAlhhInFzTUSnSRpPzY='  # 必须为 32 字节

JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = datetime.timedelta(days=30)  # 令牌有效时间
# JWT_REFRESH_DELTA = datetime.timedelta(days=30)         # 刷新令牌的有效时间
JWT_REFRESH_DELTA = datetime.timedelta(days=3)  # 剩余3天时刷新令牌

PORT = 2233

DEBUG = True

# 允许所有主机名请求
ALLOWED_HOSTS = ['*']

# 设置跨域
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False  # 改为 False
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost',
    'http://127.0.0.1',
    'http://localhost:3002',
    'http://localhost:3001',
    'http://localhost:3003',
    'http://localhost:3004',
    'http://localhost:3005',
    'http://localhost:3006',
    'https://localhost:3000',
    'https://localhost',
    'https://127.0.0.1',
    'https://localhost:3002',
    'https://localhost:3001',
    'https://localhost:3003',
    'https://localhost:3004',
    'https://localhost:3005',
    'https://localhost:3006',
    'https://192.168.43.1:3002',
    'http://localhost:5173',
    'https://localhost:2000',
    'http://localhost:2000',
'https://localhost:2001',
    'http://localhost:2001',
    'https://127.0.0.1:2001',
    'http://127.0.0.1:2001',
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# 添加信任的 CSRF 域名
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost',
    'http://127.0.0.1',
    'http://localhost:3002',
    'http://localhost:3001',
    'http://localhost:3003',
    'http://localhost:3004',
    'http://localhost:3005',
    'http://localhost:3006',
    'http://localhost:3000',
    'https://localhost:3000',
    'https://localhost',
    'https://127.0.0.1',
    'https://localhost:3002',
    'https://localhost:3001',
    'https://localhost:3003',
    'https://localhost:3004',
    'https://localhost:3005',
    'https://localhost:3006',
    'https://192.168.43.1:3002',
    'http://localhost:5173/',
    'https://localhost:2000',
    'http://localhost:2000',
    'https://localhost:2001',
    'http://localhost:2001',
    'https://127.0.0.1:2001',
    'http://127.0.0.1:2001',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'channels',
    'djangoWebServer.WebSocket',
    'views.GetUserInfo',
    'views.mysql_conn_test',
    'views.upload',
    'views.notice_control',
    'views.novel',
    'views.get_work_info',
    'views.update_userinfo',
    'views.work_interaction',
    'views.recommend',
    'views.rankling_list',
    'views.data_analysis',
    'rest_framework',  # 确保只添加一次
    'rest_framework_simplejwt',
    'views.get_browse_history',
]


ASGI_APPLICATION = 'djangoWebServer.asgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 这里
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangoWebServer.model.VerifyToken.VerifyToken',  # 通过/verify/接口来验证token是否正确
    'djangoWebServer.model.DecodeToken.DecodeToken',  # 如果请求中附加了正确的token将会解码并附加到request中
    'djangoWebServer.model.JWTRefreshMiddleware.JWTRefreshMiddleware',  # 先检查是否即将过期，过期刷新
    'djangoWebServer.model.JWTGenerateMiddleware.JWTGenerateMiddleware',  # 通过/login/接口来生成token并返回，该接口会自动拦截,

]

ROOT_URLCONF = 'djangoWebServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
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

WSGI_APPLICATION = 'djangoWebServer.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'admin',
        'USER': 'admin',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

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
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # 根据需要设置有效期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 设置 session 的有效期为 60 分钟
SESSION_COOKIE_AGE = 60 * 60  # 30 分钟 = 1800 秒

# 如果需要在浏览器关闭时过期
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


