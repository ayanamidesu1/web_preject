from django.http import JsonResponse
from django.views import View
import jwt
from django.conf import settings
from datetime import datetime, timezone
from .DecodeToken import JWTUser


class RefreshTokenView(View):
    """手动刷新 JWT 令牌"""

    def post(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('token '):
            return JsonResponse({'code': 400, 'msg': 'Token 必须作为 Authorization 头传递'}, status=400)

        token = auth_header.split(' ')[1]
        decoded_payload = self.decode_jwt(token)

        if not decoded_payload:
            return JsonResponse({'code': 401, 'msg': '无效或过期的令牌'}, status=401)

        # 刷新令牌并生成新的过期时间
        new_payload = decoded_payload.copy()
        new_payload['exp'] = datetime.now(timezone.utc) + settings.JWT_EXPIRATION_DELTA
        new_token = jwt.encode(new_payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        # 将 new_token 转换为字符串
        new_token_str = new_token.decode('utf-8')  # 解码为字符串

        return JsonResponse({
            'code': 200,
            'msg': '令牌刷新成功',
            'token': new_token_str
        }, status=200)

    def decode_jwt(self, token):
        """解码 JWT 令牌"""
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None  # 令牌过期
        except jwt.InvalidTokenError:
            return None  # 令牌无效
