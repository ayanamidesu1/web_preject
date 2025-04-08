from base_api import BaseApi
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db import transaction, connection


class GeneratePasswordCard(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            # 权限验证
            if not request.user.is_login and request.user.role not in ['admin', 'sys_admin']:
                return JsonResponse({'code': 403, 'msg': "权限问题"}, status=403)

            # 参数处理
            data = self.format_request(request)
            count = min(int(data.get('count', 10)), 10000)  # 限制最大数量
            day = min(int(data.get('day', 1)), 365)  # 限制最大天数
            price = max(float(data.get('price', 0.00000000)), 0)  # 确保非负

            # 参数校验
            if count <= 0:
                return JsonResponse({'code': 400, 'msg': '数量必须大于0'}, status=400)
            if day <= 0:
                return JsonResponse({'code': 400, 'msg': '天数必须大于0'}, status=400)

            # 计算公共值
            now = datetime.now()
            target_time = now + timedelta(days=day)
            user_id = request.user.id

            # 原生批量插入SQL（PostgreSQL语法）
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # 构建VALUES部分
                    values = []
                    params = []
                    for _ in range(count):
                        values.append("(%s, %s, %s, %s, %s, %s)")
                        params.extend([
                            str(self.get_uuid()),
                            target_time,
                            0,  # use_status
                            now,
                            user_id,
                            price
                        ])

                    # 执行批量插入
                    sql = f"""
                    INSERT INTO card_password 
                    (card_key, duration, use_status, create_time, create_user, price)
                    VALUES {','.join(values)}
                    """
                    cursor.execute(sql, params)

                    if cursor.rowcount != count:
                        raise Exception(f"插入数量不匹配，预期:{count}，实际:{cursor.rowcount}")

            self.info_log(f'成功生成{count}张密码卡', request)
            return JsonResponse({
                'code': 200,
                'msg': '生成成功',
                'count': count,
                'price': float(price),
                'expire_time': target_time.isoformat()
            }, status=200)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({
                'code': 500,
                'msg': '服务器错误',
                'detail': str(e)
            }, status=500)