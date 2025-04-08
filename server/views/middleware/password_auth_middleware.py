from datetime import timedelta, datetime

from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from cryptography.fernet import Fernet
import jwt
import json
import os

from ..log.log import Logger

# 获取加密密钥
token_key_path = os.path.join(settings.BASE_DIR, 'token_key.txt')
token_secret = open(token_key_path, 'rb').read()
cipher_suite = Fernet(token_secret)
logger = Logger()
TOKEN_EXPIRY=3600

def create_jwt_token(userid, role='front_end'):
    """生成并签名 JWT Token，设置自定义过期时间"""
    try:
        payload = {
            'userid': userid,
            'exp': timezone.now() + timedelta(seconds=TOKEN_EXPIRY),  # 使用 timezone.now()
            'role': role  # 添加 role 字段以区分前后台
        }
        # 使用 SECRET_KEY 进行编码
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        print(f'生成 JWT Token 错误: {e}')
        raise ValueError("生成 Token 失败")

def encrypt_token(token):
    """加密 JWT Token"""
    if isinstance(token, str):
        token = token.encode()  # 确保 token 是 bytes 类型
    return cipher_suite.encrypt(token).decode()

def filter_user_info(user_info):
    """过滤用户信息，去除不需要的字段"""
    fields_to_remove = {'password', 'token', 'ip_address', 'user_register', 'last_login', 'phone'}
    return {key: value for key, value in user_info.items() if key not in fields_to_remove}

class PasswordAuthMiddleware:
    MAX_ATTEMPTS = 60
    BLOCK_TIME = 30  # 锁定 30 秒
    RATE_LIMIT = 20  # 每秒最大尝试次数

    def __init__(self, get_response):
        self.get_response = get_response

    def _is_blocked(self, userid):
        """检查用户是否被锁定"""
        block_key = f"user_block_{userid}"
        block_info = cache.get(block_key)
        if block_info:
            block_time = datetime.strptime(block_info, '%Y-%m-%d %H:%M:%S')
            if datetime.now() < block_time + timedelta(seconds=self.BLOCK_TIME):
                return True
        return False

    def _record_attempt(self, userid):
        """记录用户的登录尝试"""
        attempts_key = f"user_attempts_{userid}"
        last_attempt_time_key = f"user_last_attempt_time_{userid}"

        now = datetime.now()
        last_attempt_time = cache.get(last_attempt_time_key)
        if last_attempt_time:
            last_attempt_time = datetime.strptime(last_attempt_time, '%Y-%m-%d %H:%M:%S')
        else:
            last_attempt_time = now

        # 如果距离上次尝试超过1秒，则重置计数
        if (now - last_attempt_time).total_seconds() > 1:
            cache.set(attempts_key, 0)
            cache.set(last_attempt_time_key, now.strftime('%Y-%m-%d %H:%M:%S'))

        attempts = cache.get(attempts_key, 0)
        if attempts >= self.RATE_LIMIT:
            return False
        else:
            cache.set(attempts_key, attempts + 1)
            return True

    def _record_failed_attempt(self, userid):
        """记录失败的登录尝试，如果达到最大次数，则锁定用户"""
        attempts_key = f"user_failed_attempts_{userid}"
        failed_attempts = cache.get(attempts_key, 0)
        if failed_attempts >= self.MAX_ATTEMPTS:
            block_time = datetime.now()
            cache.set(f"user_block_{userid}", block_time.strftime('%Y-%m-%d %H:%M:%S'))
            cache.set(attempts_key, 0)
        else:
            cache.set(attempts_key, failed_attempts + 1)

    def _authenticate_user(self, userid, password, login_type, username=None, email=None, role='front_end'):
        """根据登录类型选择 SQL 查询语句并执行"""
        if login_type == 'front_end':
            query = '''SELECT * FROM users WHERE (userid=%s OR username=%s OR email=%s) AND password=%s'''
            params = (userid, username, email, password)
        elif login_type == 'back_end':
            query = '''SELECT * FROM users WHERE userid=%s AND password=%s AND (role='super_admin' OR role='admin') '''
            params = (userid, password)
        else:
            return None, None

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                user_data = cursor.fetchone()
                if user_data:
                    columns = [desc[0] for desc in cursor.description]
                    user_info = dict(zip(columns, user_data))
                    # 过滤用户信息
                    userid = user_info['userid']
                    filtered_user_info = filter_user_info(user_info)
                    return filtered_user_info, create_jwt_token(userid, role)
                else:
                    return None, None
        except Exception as e:
            logger.error(f'数据库查询错误: {str(e)}')
            raise

    def password_auth(self, request):
        if request.content_type == 'multipart/form-data':
            return None
        auth_header = request.headers.get('Authorization', None)
        if auth_header and auth_header.startswith('Bearer '):
            return None

        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的请求体'}, status=400)

        userid = data.get('userid', None)
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)
        login_type = data.get('login_type', 'front_end')

        if not password or (login_type == 'front_end' and not any([userid, username, email])) or (
                login_type == 'back_end' and not userid):
            return JsonResponse({'status': 'error', 'message': '认证信息不完整'}, status=400)

        if self._is_blocked(userid):
            return JsonResponse({'status': 'error', 'message': '用户已被锁定，请稍后再试'}, status=429)

        if not self._record_attempt(userid):
            return JsonResponse({'status': 'error', 'message': '操作过于频繁，请稍后再试'}, status=429)

        user_info, token = self._authenticate_user(userid, password, login_type, username, email, login_type)

        if not token:
            return JsonResponse({'status': 'error', 'message': '认证失败'}, status=401)
        e_token = encrypt_token(token)
        if user_info:
            request.userinfo = json.dumps(user_info)
            request.userid = userid
            request.token = e_token
            request.is_login = True
            request.role = login_type
            return None
        else:
            self._record_failed_attempt(userid)
            logger.warning(f'认证失败: 用户 {userid}, 登录类型 {login_type}')
            return JsonResponse({'status': 'error', 'message': '认证失败'}, status=401)

    def __call__(self, request):
        if request.content_type != 'multipart/form-data':
            if request.method == 'POST':
                response = self.password_auth(request)
                if response:
                    return response
            return self.get_response(request)
        else:
            return self.get_response(request)

