import jwt
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from log.log import Logger
from django.conf import settings
from django.db import connection, transaction
from datetime import datetime

logger = Logger()


class VerifyToken(MiddlewareMixin):
    def process_request(self, request):
        # 只处理 /verify/ 请求
        if request.method != 'POST' or request.path != '/verify/':
            return None

        try:
            # Token验证
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if not auth_header or not auth_header.startswith('token '):
                return JsonResponse({'code': 400, 'msg': 'Token 必须作为 Authorization 头传递'}, status=400)

            token = auth_header.split(' ')[1]
            if not self.decode_jwt(token):
                request.is_login = False
                return JsonResponse({'code': 401, 'msg': '无效或过期的令牌'}, status=401)

            return JsonResponse({'code': 200, 'msg': 'Token 验证通过'}, status=200)

        except Exception as e:
            logger.error(f"Token 验证失败: {e}")
            return JsonResponse({'code': 500, 'msg': '服务器内部错误'}, status=500)

    def decode_jwt(self, token):
        try:
            return jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_exp": True}
            )
        except jwt.ExpiredSignatureError:
            logger.warning(f"Token 已过期: {token}")
            return None
        except jwt.InvalidTokenError:
            logger.warning(f"无效 Token: {token}")
            return None
        except Exception as e:
            logger.error(f"JWT 解码失败: {e}")
            return None