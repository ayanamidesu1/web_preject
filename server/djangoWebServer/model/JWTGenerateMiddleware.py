import json
import jwt
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from ..log.log import Logger
from datetime import datetime, timezone
from django.db import connection
from django.conf import settings

logger = Logger()


class JWTGenerateMiddleware(MiddlewareMixin):
    """JWT 生成中间件"""

    LOGIN_PATH = '/login/'  # 定义登录路径

    def process_request(self, request):
        # 仅处理特定的登录路径
        if request.method != 'POST' or request.path != self.LOGIN_PATH:
            return None  # 非 POST 请求或路径不匹配时不处理

        try:
            data = json.loads(request.body.decode('utf-8'))
            now = datetime.now(timezone.utc)
            login_key = data.get('login_key')
            password = data.get('password')

            if not login_key or not password:
                return JsonResponse({'code': 400, 'msg': '参数错误'}, status=400)

            # 查询数据库
            with connection.cursor() as cursor:
                login_sql = '''
                    SELECT * FROM users 
                    WHERE (user_id=%s OR username=%s OR email=%s OR phone=%s) AND password=%s
                '''
                cursor.execute(login_sql, (login_key, login_key, login_key, login_key, password))
                result = cursor.fetchone()

                if not result:
                    return JsonResponse({'code': 400, 'msg': '用户名或密码错误'}, status=400)

                # 将查询结果格式化为字典
                user_data = dict(zip([col[0] for col in cursor.description], result))
                #print(user_data)

                # 生成 JWT payload
                payload = {
                    'user_id': user_data.get('user_id'),
                    'username': user_data.get('username'),
                    'email': user_data.get('email'),
                    'phone': user_data.get('phone'),
                    'sex': user_data.get('sex'),
                    'avatar': user_data.get('avatar'),
                    'user_level': user_data.get('user_level',1),
                    'background': user_data.get('background'),
                    'now': now.isoformat(),
                    'is_login': True,
                    'status':user_data.get('status',0)
                }

                # 返回带有 JWT 的响应
                token = self.generate_jwt(payload)
                return JsonResponse({
                    'code': 200,
                    'msg': '登录成功',
                    'token': token
                }, status=200)

        except Exception as e:
            logger.error(f"JWT生成失败: {e}")
            return JsonResponse({'code': 500, 'msg': '服务器内部错误'}, status=500)

    def generate_jwt(self, payload, expiration=None):
        """生成 JWT 令牌"""
        payload['exp'] = datetime.now(timezone.utc) + (expiration or settings.JWT_EXPIRATION_DELTA)
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return token if isinstance(token, str) else token.decode('utf-8')  # 确保返回字符串

    def decode_jwt(self, token):
        """解码 JWT 令牌"""
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None  # 令牌过期
        except jwt.InvalidTokenError:
            return None  # 令牌无效
