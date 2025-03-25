import jwt
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.core.cache import cache
from cryptography.fernet import Fernet
from .log.log import Logger
import json

TOKEN_EXPIRY = 3600  # Token 有效期为 1 小时

# 秘钥，用于加密和解密前端的 Token
SECRET_KEY = b'lgYdcCA1tc5odYAkri_fYg2UuAlhhInFzTUSnSRpPzY='  # 必须为 32 字节
cipher_suite = Fernet(SECRET_KEY)


def create_jwt_token(userid):
    """生成并签名 JWT Token，设置自定义过期时间"""
    try:
        payload = {
            'userid': userid,
            'exp': timezone.now() + timedelta(seconds=TOKEN_EXPIRY)  # 使用 timezone.now()
        }
        # 使用 SECRET_KEY 进行编码
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        print(f'生成 JWT Token 错误: {e}')
        raise ValueError("生成 Token 失败")


def decode_jwt_token(token):
    """解码 JWT Token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token 已过期")
    except jwt.InvalidTokenError:
        raise ValueError("无效的 Token")


def encrypt_token(token):
    """加密 JWT Token"""
    if isinstance(token, str):
        token = token.encode()  # 确保 token 是 bytes 类型
    return cipher_suite.encrypt(token).decode()

def decrypt_token(encrypted_token):
    """解密 JWT Token"""
    if isinstance(encrypted_token, str):
        encrypted_token = encrypted_token.encode()  # 确保 encrypted_token 是 bytes 类型
    return cipher_suite.decrypt(encrypted_token).decode()



class Authentication(View):
    logger = Logger()
    MAX_ATTEMPTS = 100
    BLOCK_TIME = 1  # 秒
    RATE_LIMIT = 20  # 每秒允许的最大尝试次数

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = None  # 初始化请求对象

    def set_request(self, request):
        self.request = request

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

        # 如果超过 1 秒，重置尝试次数
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
        """记录失败的登录尝试，如果需要则锁定用户"""
        attempts_key = f"user_failed_attempts_{userid}"
        failed_attempts = cache.get(attempts_key, 0)
        if failed_attempts >= self.MAX_ATTEMPTS:
            block_time = datetime.now()
            cache.set(f"user_block_{userid}", block_time.strftime('%Y-%m-%d %H:%M:%S'))
            cache.set(attempts_key, 0)
        else:
            cache.set(attempts_key, failed_attempts + 1)

    def _fetch_user(self, cursor, sql, params):
        """从数据库中获取用户数据"""
        cursor.execute(sql, params)
        return cursor.fetchone()

    def authenticate_user(self, token=None, userid=None, password=None):
        """用户认证方法"""
        try:
            with connection.cursor() as cursor:
                if userid is not None or password is not None:
                    try:
                        if self._is_blocked(userid):
                            return json.dumps({'status': 'error', 'message': '用户已被锁定，请稍后再试',
                                               'token': '', 'status_code': 429})

                        # 基于 ID 和密码的认证
                        get_user_sql = '''
                            SELECT userid, account_permissions FROM users WHERE userid=%s AND password=%s
                        '''
                        if not self._record_attempt(userid):
                            return json.dumps({'status': 'error', 'message': '操作过于频繁，请稍后再试', 'token': '',
                                               'status_code': 429})

                        row = self._fetch_user(cursor, get_user_sql, (str(userid), str(password)))

                        if not row:
                            self._record_failed_attempt(userid)
                            return json.dumps({'status': 'error', 'message': '用户名或密码错误',
                                               'token': '', 'status_code': 401})

                        if row and row[1] in ['1', '2']:
                            # 生成 JWT Token 并加密
                            userid = row[0]  # 获取用户对象
                            new_token = create_jwt_token(userid)
                            encrypted_token = encrypt_token(new_token)
                            account_permissions = row[1]
                            # 获取登录用户信息
                            get_userinfo_sql = 'SELECT * FROM users WHERE userid=%s'
                            cursor.execute(get_userinfo_sql, (userid,))
                            user_info = cursor.fetchone()
                            columns = [desc[0] for desc in cursor.description]
                            user_info = dict(zip(columns, user_info))
                            return json.dumps({'status': 'success', 'token': encrypted_token,
                                               'status_code': 200, 'is_login': 1,
                                               'account_permissions': account_permissions,
                                               'user_info': user_info})
                        else:
                            self._record_failed_attempt(userid)
                            return json.dumps({'status': 'error', 'message': '非授权用户，请联系管理员',
                                               'token': '', 'status_code': 403})
                    except Exception as e:
                        print('\n用户认证错误：', e)
                        self.logger.error('用户认证错误：' + str(e))
                        return json.dumps({'status': 'error', 'message': '服务器错误', 'token': '',
                                           'status_code': 500})

                if token is not None and token != '':
                    # 验证 JWT Token
                    try:
                        decrypted_token = decrypt_token(token)
                        payload = decode_jwt_token(decrypted_token)
                        userid = payload.get('userid')

                        # 获取用户权限
                        get_user_sql = '''
                            SELECT account_permissions FROM users WHERE userid=%s
                        '''
                        # 获取登录用户信息
                        get_userinfo_sql = 'SELECT * FROM users WHERE userid=%s'
                        cursor.execute(get_userinfo_sql, (str(userid),))
                        user_info = cursor.fetchone()
                        columns = [desc[0] for desc in cursor.description]
                        user_info = dict(zip(columns, user_info))
                        cursor.execute(get_user_sql, (str(userid),))
                        account_permissions = cursor.fetchone()[0]

                        # 生成新的 Token
                        new_token = create_jwt_token(userid)
                        encrypted_new_token = encrypt_token(new_token)
                        return json.dumps({'status': 'success', 'token': encrypted_new_token, 'status_code': 200,
                                           'data': '', 'is_login': 1, 'account_permissions': account_permissions,
                                           'user_info': user_info})
                    except jwt.ExpiredSignatureError:
                        return json.dumps({'status': 'error', 'message': 'Token 已过期', 'token': '',
                                           'status_code': 401, 'is_login': 0})
                    except jwt.InvalidTokenError:
                        return json.dumps({'status': 'error', 'message': '无效的 Token', 'token': '',
                                           'status_code': 400, 'is_login': 0})
                    except Exception as e:
                        print('\n', e)
                        self.logger.error(f"Token 验证错误: {e}")
                        return json.dumps({'status': 'error', 'message': '服务器错误', 'token': '',
                                           'status_code': 500, 'is_login': 0})

                else:
                    return json.dumps({'status': 'error', 'message': '缺少认证信息', 'status_code': 400})

        except Exception as e:
            print('\n', e)
            self.logger.error(f"认证过程中出错: {e}")
            return json.dumps({'status': 'error', 'message': '认证过程中出错', 'status_code': 500})
