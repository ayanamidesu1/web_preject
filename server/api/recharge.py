from base_api import BaseApi
from django.http import JsonResponse
from datetime import datetime
import decimal


class Recharge(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            # 1. 基础验证
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'}, status=401)

            if not (card_password := self.format_request(request).get('card_password')):
                return JsonResponse({'code': 400, 'msg': '请输入卡密'}, status=400)

            # 2. 查询并锁定卡密
            if not (card_info := self.execute_sql(
                    'SELECT * FROM card_password WHERE card_key=%s FOR UPDATE',
                    (card_password,),
                    return_results=True
            )):
                return JsonResponse({'code': 400, 'msg': '卡密不存在或查询失败'}, status=400)

            # 3. 验证卡密状态
            now = datetime.now()
            if card_info[0].get('use_status') == 1:
                return JsonResponse({'code': 400, 'msg': '卡密已被使用'}, status=400)

            # 4. 检查有效期
            try:
                duration_str = str(card_info[0]['duration'])
                expire_time = (
                    datetime.strptime(duration_str, '%Y-%m-%d %H:%M:%S.%f')
                    if '.' in duration_str
                    else datetime.strptime(duration_str, '%Y-%m-%d %H:%M:%S')
                )
                if expire_time < now:
                    return JsonResponse({'code': 400, 'msg': f'卡密已过期（有效期至 {expire_time}）'}, status=400)
            except ValueError:
                return JsonResponse({'code': 400, 'msg': f'卡密有效期格式错误：{card_info[0]["duration"]}'}, status=400)

            # 5. 处理金额
            try:
                price = decimal.Decimal(str(card_info[0]['price'])).quantize(decimal.Decimal('0.00000000'))
            except decimal.InvalidOperation:
                return JsonResponse({'code': 400, 'msg': f'无效的金额格式：{card_info[0]["price"]}'}, status=400)

            # 6. 执行充值流程（每个步骤独立验证）
            user_id = request.user.id

            # 6.1 更新余额
            if self.execute_sql(
                    'UPDATE money SET balance=balance+%s, last_update=%s WHERE user_id=%s',
                    (price, now, user_id),
                    return_results=False
            ) != 1:
                return JsonResponse({'code': 500, 'msg': '用户余额更新失败'}, status=500)

            # 6.2 标记卡密已使用
            if self.execute_sql(
                    'UPDATE card_password SET use_status=1 WHERE card_key=%s',
                    (card_password,),
                    return_results=False
            ) != 1:
                return JsonResponse({'code': 500, 'msg': '卡密状态更新失败'}, status=500)

            # 6.3 创建订单记录
            if self.execute_sql(
                    'INSERT INTO `order` (type, amount_of_money, user_id, time, goods_id, status, back) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    ['recharge', float(price), user_id, now, card_info[0]['card_key'], 1, '账户余额充值'],
                    return_results=False
            ) != 1:
                return JsonResponse({'code': 500, 'msg': '订单记录创建失败'}, status=500)

            return JsonResponse({'code': 200, 'msg': '充值成功'})

        except Exception as e:
            self.error_log(f"系统异常: {str(e)}", request)
            return JsonResponse({'code': 500, 'msg': f'系统处理错误: {str(e)}'}, status=500)