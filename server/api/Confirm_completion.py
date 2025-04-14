from django.http import JsonResponse
from base_api import BaseApi
from datetime import datetime


class ConfirmCompletion(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if self.check_user(request):
                return self.check_user(request)
            # 更新订单状态
            data = self.format_request(request)
            order_id = data.get('order_id')
            if not order_id:
                return JsonResponse({'code': 400, 'msg': '缺少参数'}, status=400)
            update_order_status_sql = '''update `order` set status=1 where `order`.id=%s and user_id=%s'''
            # 获取被委托者ID以及订单金额并更新委托者钱包余额
            sql = '''select target_user_id ,amount_of_money from `order` where id=%s and user_id=%s'''
            result = self.execute_sql(sql, (order_id, request.user.id), True)[0]
            # 更新钱包余额
            now = datetime.now()
            amount = float(result.get('amount_of_money'))
            update_wallet_sql = '''update money set balance=(balance+%s),last_update=%s where user_id=%s'''
            if self.execute_sql(update_order_status_sql, (order_id, request.user.id), False) == 1:
                if self.execute_sql(update_wallet_sql, [amount, now, result.get('target_user_id')]) == 1:
                    return JsonResponse({'code': 200, 'msg': '订单确认成功'}, status=200)

                else:
                    return JsonResponse({'code': 400, 'msg': '订单确认失败，目标用户钱包更新失败'}, status=400)
            else:
                return JsonResponse({'code': 400, 'msg': '订单确认失败'}, status=400)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
