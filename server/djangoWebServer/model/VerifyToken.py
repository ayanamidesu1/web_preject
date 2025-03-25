import jwt
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from ..log.log import Logger
from django.conf import settings

logger = Logger()


class VerifyToken(MiddlewareMixin):
    def process_request(self, request):
        print(request.path)
        # 只处理 /verify/ 请求，其他请求不做处理
        if request.method != 'POST' or request.path != '/verify/':
            print('不处理')
            return None  # 非 POST 请求或路径不匹配时不处理
        if request.path == '/verify/':
            print('验证Token')
            try:
                # 从请求头中提取 Authorization 字段
                auth_header = request.META.get('HTTP_AUTHORIZATION')
                if auth_header is None or not auth_header.startswith('token '):
                    return JsonResponse({'code': 400, 'msg': 'Token 必须作为 Authorization 头传递'}, status=400)

                # 提取 Token 部分
                token = auth_header.split(' ')[1]

                # 解码并验证 Token
                decoded_payload = self.decode_jwt(token)
                if decoded_payload is None:
                    # 设置request的is_login为False
                    request.is_login = False
                    return JsonResponse({'code': 401, 'msg': '无效或过期的令牌'}, status=401)

                # 如果验证通过，返回验证成功的响应
                return JsonResponse({'code': 200, 'msg': 'Token 验证通过'}, status=200)

            except Exception as e:
                logger.error(f"Token 验证失败: {e}")
                return JsonResponse({'code': 500, 'msg': '服务器内部错误'}, status=500)
        return None

    def decode_jwt(self, token):
        """解码并验证 JWT 令牌"""
        try:
            # 解码时自动验证过期时间
            decoded_payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_exp": True}  # 自动验证过期时间
            )
            return decoded_payload
        except jwt.ExpiredSignatureError:
            # Token 已过期
            logger.warning(f"Token 已过期: {token}")
            return None
        except jwt.InvalidTokenError:
            # 无效 Token
            logger.warning(f"无效 Token: {token}")
            return None
        except Exception as e:
            # 其他解码错误
            logger.error(f"JWT 解码失败: {e}")
            return None
