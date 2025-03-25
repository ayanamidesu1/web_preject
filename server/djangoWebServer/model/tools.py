import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings


# 生成token
def generate_jwt(payload, expiration=None):
    """生成JWT令牌"""
    payload['exp'] = datetime.now(timezone.utc) + (expiration or settings.JWT_EXPIRATION_DELTA)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


# 解码token
def decode_jwt(token):
    """解码JWT令牌"""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None  # 令牌过期
    except jwt.InvalidTokenError:
        return None  # 令牌无效
