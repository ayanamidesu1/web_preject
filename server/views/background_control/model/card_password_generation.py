from cryptography.fernet import Fernet
import uuid
from django.db import connection
from django.http import JsonResponse
from django.views import View
from .log.log import Logger
from datetime import datetime, timedelta
import base64

# 从文件中加载密钥
def load_key():
    return open('secret.key', 'rb').read()

# 加载加密密钥
fernet = Fernet(load_key())

# 时间长度常量
card_scale_day = 1
card_scale_week = 7
card_scale_month = 30
card_scale_year = 365

class CardPasswordGeneration(View):
    logger = Logger()

    def _encrypt_data(self, data: str) -> str:
        """加密数据"""
        encrypted_data = fernet.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

    def _decrypt_data(self, encrypted_data: str) -> str:
        """解密数据"""
        encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_data)
        decrypted_data = fernet.decrypt(encrypted_data_bytes).decode('utf-8')
        return decrypted_data

    # 生成卡密并加密相关信息
    def _generate_card_password(self, card_scale, userid):
        now = datetime.now()
        time_str = now.strftime('%Y%m%d%H%M%S')  # 年月日时分秒作为时间戳
        duration_str = f'{card_scale:03d}'  # 时长编码为3位数
        user_str = f'{userid:06d}'  # 用户ID编码为6位数

        # 使用uuid4生成随机部分
        random_part = str(uuid.uuid4()).replace('-', '')[:8]  # 截取前8位作为随机部分

        # 将时间、时长和用户ID加密
        encrypted_time = self._encrypt_data(time_str)
        encrypted_duration = self._encrypt_data(duration_str)
        encrypted_user = self._encrypt_data(user_str)

        # 最终卡密格式：加密时间 + 加密时长 + 加密用户ID + 随机部分
        card_password = f'{encrypted_time}{encrypted_duration}{encrypted_user}{random_part}'

        return card_password

    # 解析卡密并解密相关信息
    def _parse_card_password(self, card_password):
        # 分割卡密，假设加密部分长度固定，解密出时间、时长、用户ID等信息
        encrypted_time = card_password[:44]  # 加密的时间长度为44位
        encrypted_duration = card_password[44:88]  # 加密的时长长度为44位
        encrypted_user = card_password[88:132]  # 加密的用户ID长度为44位

        random_part = card_password[132:]  # 随机部分

        # 解密
        create_time = datetime.strptime(self._decrypt_data(encrypted_time), '%Y%m%d%H%M%S')
        duration = int(self._decrypt_data(encrypted_duration))
        userid = int(self._decrypt_data(encrypted_user))

        return {
            'create_time': create_time,
            'duration': duration,
            'userid': userid,
            'random_part': random_part
        }

    # 处理POST请求
    def post(self, request, *args, **kwargs):
        userid = getattr(request, 'userid', None)
        is_authenticated = getattr(request, 'is_authenticated', None)

        if not is_authenticated:
            self.logger.warning(f'未登录用户尝试访问：{self._request_path(request)}')
            return JsonResponse({'status': 'fail', 'message': '未登录'}, status=401)

        # 检查用户权限
        with connection.cursor() as cursor:
            cursor.execute('SELECT account_permissions FROM users WHERE userid=%s', [userid])
            account_permissions = cursor.fetchone()

            if not account_permissions or account_permissions[0] not in ['1', '2', 1, 2]:
                self.logger.warning(f'用户权限不足：{self._request_path(request)}')
                return JsonResponse({'status': 'fail', 'message': '权限不足'}, status=403)

            # 批量生成卡密
            sql = '''
                INSERT INTO card_password (card_key, duration, use_status, create_time, create_user) 
                VALUES (%s, %s, %s, %s, %s)
            '''
            create_time = datetime.now()

            # 生成每种卡密100份
            for card_scale in [card_scale_day, card_scale_week, card_scale_month, card_scale_year]:
                for _ in range(100):
                    card_password = self._generate_card_password(card_scale, userid)
                    cursor.execute(sql, [card_password, card_scale, 'unused', create_time, userid])

            self.logger.info(f'{userid}成功生成了卡密。')
            return JsonResponse({'status': 'success', 'message': '卡密生成成功'}, status=200)

    def _request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        content = request.body.decode('utf-8')
        return f'{request_ip}在{now}请求了{request_path}, 请求内容为：{content}'
