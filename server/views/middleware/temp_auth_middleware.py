from datetime import timedelta, datetime

from cryptography.fernet import Fernet
from django.conf import settings
from django.utils import timezone

from ..log.log import Logger
from django.http import JsonResponse
import jwt
import json
import uuid
from django.db import connection
import os

# 初始化日志记录器
logger = Logger()

# 获取加密密钥
token_key_path = os.path.join(settings.BASE_DIR, 'token_key.txt')
token_secret = open(token_key_path, 'rb').read()
cipher_suite = Fernet(token_secret)
TOKEN_EXPIRY=3600

# SQL 语句
create_temp_user_sql = '''
    INSERT INTO users (username, userid, password, vip, account_status, account_permissions, last_login, ip_address) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
'''
delete_temp_user_sql = '''
    DELETE FROM users WHERE userid=%s
'''
count_temp_users_by_ip_sql = '''
    SELECT COUNT(*) FROM users WHERE ip_address=%s AND account_permissions=-1
'''

# 创建 JWT Token
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

# 生成随机 UUID 以供临时用户的 ID 和密码设置
def generate_uuid():
    return str(uuid.uuid4())

class TempAuthMiddleware:
    MAX_TEMP_USERS_PER_IP = 10  # 每个IP最多创建的临时账户数量

    def __init__(self, get_response):
        self.get_response = get_response

    def create_temp_user(self, username, userid, password, vip, account_status, account_permissions, ip_address):
        try:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with connection.cursor() as cursor:
                cursor.execute(create_temp_user_sql,
                               (username, userid, password, vip, account_status, account_permissions, now, ip_address))
                return cursor.rowcount == 1
        except Exception as e:
            logger.error(f"创建临时用户失败: {e}")
            return False

    def delete_temp_user(self, userid):
        try:
            with connection.cursor() as cursor:
                cursor.execute(delete_temp_user_sql, (userid,))
                return cursor.rowcount == 1
        except Exception as e:
            logger.error(f"删除临时用户失败: {e}")
            return False

    def count_temp_users_by_ip(self, ip_address):
        try:
            with connection.cursor() as cursor:
                cursor.execute(count_temp_users_by_ip_sql, (ip_address,))
                return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"统计临时用户失败: {e}")
            return 0

    def __call__(self, request):
        try:
            if request.content_type == 'multipart/form-data':
                return self.get_response(request)
            # 如果请求已经通过认证，则跳过临时用户创建
            if hasattr(request, 'is_login') and request.is_login:
                return self.get_response(request)

            # 获取客户端的IP地址
            ip_address = request.META.get('REMOTE_ADDR')

            # 检查该IP地址是否已经创建了超过限制数量的临时账户
            if self.count_temp_users_by_ip(ip_address) >= self.MAX_TEMP_USERS_PER_IP:
                return JsonResponse({'status': 'error', 'message': '该IP地址创建的临时账户数量已达到上限'}, status=429)

            # 创建临时用户
            userid = generate_uuid()
            username = f"temp_{userid[:8]}"
            password = generate_uuid()  # 临时用户使用随机生成的密码
            vip = 0  # 临时用户的 VIP 状态为 0
            account_status = 2  # 临时用户状态设置为 2，表示禁言
            account_permissions = -1  # 临时用户权限为 -1

            if self.create_temp_user(username, userid, password, vip, account_status, account_permissions, ip_address):
                # 创建成功，将用户信息附加到请求中
                request.userid = userid
                new_token = encrypt_token(create_jwt_token(userid))
                c_token=encrypt_token(new_token)
                request.token = c_token
                request.is_login = True
            else:
                return JsonResponse({'status': 'error', 'message': '创建临时用户失败'}, status=500)

        except Exception as e:
            logger.error(f'服务器错误: {str(e)}')
            return JsonResponse({'status': 'error', 'message': f'服务器错误: {str(e)}'}, status=500)

        return self.get_response(request)

    def process_response(self, request, response):
        try:
            if hasattr(request, 'userid') and request.userid:
                self.delete_temp_user(request.userid)
        except Exception as e:
            logger.error(f"处理响应失败: {e}")

        return response

    # 定期清理过期的临时用户（可由定时任务调用）
    def clean_up_expired_temp_users(self):
        try:
            with connection.cursor() as cursor:
                delete_expired_sql = '''
                    DELETE FROM users 
                    WHERE account_permissions = -1 AND account_status = 2 AND last_login < %s
                '''
                cursor.execute(delete_expired_sql, (datetime.now() - timedelta(days=3),))
        except Exception as e:
            logger.error(f"清理过期临时用户失败: {e}")
