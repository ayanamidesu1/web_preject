import json
import jwt
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from ..log.log import Logger
from datetime import datetime, timezone
from django.conf import settings

logger = Logger()

# 创建自定义用户对象类
class JWTUser:
    def __init__(self, payload):
        # 将 JWT 解码后的字段映射为对象属性
        self.id = payload.get('user_id')
        self.username = payload.get('username')
        self.email = payload.get('email')
        self.phone = payload.get('phone')
        self.sex = payload.get('sex')
        self.avatar = payload.get('avatar')
        self.user_level = payload.get('user_level')
        self.background = payload.get('background')
        self.is_login = payload.get('is_login', False)
        self.status = payload.get('status',0)

    def __str__(self):
        return (f"JWTUser(id={self.id}, username={self.username}, "
                f"email={self.email}, phone={self.phone}, "
                f"sex={self.sex}, avatar={self.avatar}, "
                f"user_level={self.user_level}, background={self.background},is_login={self.is_login},"
                f"status={self.status})")

class DecodeToken(MiddlewareMixin):
    """JWT 解码中间件"""

    def process_request(self, request):
        try:
            # 从请求头中提取 Authorization 字段
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header is None or not auth_header.startswith('token '):
                # 未提供 Token，设置默认匿名用户对象
                request.user = JWTUser({})
                request.user.is_login = False
                print('未提供Token，不处理')
                return None

            # 提取 Token 部分
            token = auth_header.split(' ')[1]

            # 解码 Token
            decoded_payload = self.decode_jwt(token)
            if decoded_payload is None:
                return JsonResponse({'code': 401, 'msg': '无效或过期的令牌'}, status=401)

            # 将解码后的用户信息作为 JWTUser 对象附加到 request.user
            request.user = JWTUser(decoded_payload)
            request.user.is_login = True
            return None  # 允许请求继续

        except Exception as e:
            logger.error(f"Token 解码失败: {e}")
            return JsonResponse({'code': 500, 'msg': '服务器内部错误'}, status=500)

    def decode_jwt(self, token):
        """解码 JWT 令牌"""
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None  # 令牌过期
        except jwt.InvalidTokenError:
            return None  # 令牌无效
