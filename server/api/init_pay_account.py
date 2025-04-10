from datetime import datetime
from base_api import BaseApi
from django.http import JsonResponse


class InitPayAccount(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            # 1. 验证用户登录状态
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'}, status=401)

            # 2. 获取并验证请求数据
            data = self.format_request(request)
            pay_password = data.get('pay_password')

            # 3. 验证支付密码格式（测试阶段：6位纯数字）
            if not (pay_password and len(pay_password) == 6 and pay_password.isdigit()):
                return JsonResponse({'code': 400, 'msg': '支付密码必须为6位数字'}, status=400)

            # 4. 检查是否已初始化过支付账户
            user_id = request.user.id
            check_sql = "SELECT 1 FROM admin.money WHERE user_id = %s LIMIT 1"
            if self.execute_sql(check_sql, (user_id,), True):  # 直接判断结果列表是否非空
                return JsonResponse({'code': 400, 'msg': '支付账户已存在'}, status=400)

            # 5. 初始化支付账户（测试阶段存储明文密码）
            sql = '''
            INSERT INTO admin.money 
            (user_id, balance, last_update, pay_password) 
            VALUES (%s, %s, %s, %s)
            '''
            now = datetime.now()
            balance = float(0.00)

            if self.execute_sql(sql, (user_id, balance, now, pay_password), False) == 1:
                return JsonResponse({'code': 200, 'msg': '初始化成功'}, status=200)

            return JsonResponse({'code': 400, 'msg': '初始化失败'}, status=400)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)