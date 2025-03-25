from datetime import timedelta, datetime

from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
import jwt
import json
import os
from cryptography.fernet import Fernet
from ..log.log import Logger

# 初始化日志记录器
logger = Logger()

# 获取加密密钥
token_key_path = os.path.join(settings.BASE_DIR, 'token_key.txt')
token_secret = open(token_key_path, 'rb').read()
cipher_suite = Fernet(token_secret)

TOKEN_EXPIRY=3600*24

def create_jwt_token(userid,role='front_end'):
    """生成并签名 JWT Token，设置自定义过期时间"""
    try:
        payload = {
            'userid': userid,
            'exp': timezone.now() + timedelta(seconds=TOKEN_EXPIRY),  # 使用 timezone.now()
            'role': role
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


class TokenAuthMiddleware:
    """Token 认证中间件"""

    def __init__(self, get_response):
        self.get_response = get_response

    def token_auth(self, request):
        """Token 认证逻辑"""
        try:
            if request.content_type == 'multipart/form-data':
                return None
            # 如果请求已经附带了用户信息和 token，直接返回
            if hasattr(request, 'userinfo') and hasattr(request, 'token') and hasattr(request, 'is_authenticated'):
                request.userinfo = json.loads(request.userinfo)
                return None

            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                # 解密 Token
                decrypted_token = decrypt_token(token)
                # 解码 JWT
                decoded_token = decode_jwt_token(decrypted_token)
                if decoded_token:
                    userid = decoded_token['userid']
                    role = decoded_token.get('role', 'front_end')
                    # 每次重新生成一个新 token
                    new_token = create_jwt_token(userid, role)
                    encrypted_new_token = encrypt_token(new_token)
                    # 更新 request 对象
                    request.userid = userid
                    request.role = role
                    request.token = encrypted_new_token  # 使用新生成并加密的 token
                    request.is_authenticated = True

                    return None
                else:
                    return JsonResponse({'status': 'error', 'message': 'Token 无效或已过期'}, status=401)
            return None

        except Exception as e:
            print(e)
            logger.error(f'服务器错误: {str(e)}')
            return JsonResponse({'status': 'error', 'message': f'服务器错误: {str(e)}'}, status=500)

    def __call__(self, request):
        """处理请求"""
        if request.content_type != 'multipart/form-data':
            if request.method == 'POST':
                response = self.token_auth(request)
                if response:
                    return response
            return self.get_response(request)
        return self.get_response(request)
