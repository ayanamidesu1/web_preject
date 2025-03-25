import json
import jwt
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

from .DecodeToken import JWTUser
from ..log.log import Logger
from datetime import datetime, timezone, timedelta
from django.conf import settings

logger = Logger()


class JWTRefreshMiddleware(MiddlewareMixin):
    """JWT 刷新中间件"""

    def process_request(self, request):
        # 从请求头中提取 Authorization 字段
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header is None or not auth_header.startswith('token '):
            print('token为空')
            return None  # 未提供 Token，允许继续其他非认证相关请求
        print('刷新token')
        token = auth_header.split(' ')[1]
        decoded_payload = self.decode_jwt(token)

        if not decoded_payload:
            return JsonResponse({'code': 401, 'msg': '无效或过期的令牌'}, status=401)

        # 检查是否需要刷新 Token
        exp_time = datetime.fromtimestamp(decoded_payload['exp'], timezone.utc)
        remaining_time = exp_time - datetime.now(timezone.utc)

        if remaining_time < settings.JWT_REFRESH_DELTA:  # 如果剩余时间小于刷新时间间隔
            # 刷新令牌并生成新的过期时间
            new_payload = decoded_payload.copy()
            new_payload['exp'] = datetime.now(timezone.utc) + settings.JWT_EXPIRATION_DELTA
            new_token = jwt.encode(new_payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

            # 将新的 Token 添加到响应头
            request.META['HTTP_AUTHORIZATION'] = f'token {new_token}'

        # 将解码后的用户信息作为 JWTUser 对象附加到 request.user
        request.user = JWTUser(decoded_payload)  # 使用之前定义的 JWTUser 类
        return None  # 允许请求继续

    def decode_jwt(self, token):
        """解码 JWT 令牌"""
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None  # 令牌过期
        except jwt.InvalidTokenError:
            return None  # 令牌无效
