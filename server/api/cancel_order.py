from base_api import BaseApi
from django.http import JsonResponse
from datetime import datetime

class CancelOrder(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录', 'data': None}, status=401)

            data = self.format_request(request)
            order_id = data.get('order_id')

            if not order_id:
                return JsonResponse({'code': 400, 'msg': '订单ID不能为空', 'data': None}, status=400)

            # 查询订单是否存在及状态
            check_sql = 'SELECT id, status, amount_of_money, user_id FROM `order` WHERE id = %s LIMIT 1'
            result = self.execute_sql(check_sql, [order_id], True)

            if not result:
                return JsonResponse({'code': 404, 'msg': '订单不存在', 'data': None}, status=404)

            order = result[0]
            if order['status'] == 0:
                return JsonResponse({'code': 400, 'msg': '订单已取消，无需重复操作', 'data': None}, status=400)

            amount = float(order['amount_of_money'])
            user_id = order['user_id']
            now = datetime.now()

            # 1. 取消订单
            update_order_sql = 'UPDATE `order` SET status = 0 WHERE id = %s'
            updated = self.execute_sql(update_order_sql, [order_id], False)

            if updated != 1:
                return JsonResponse({'code': 500, 'msg': '订单取消失败', 'data': None}, status=500)

            # 2. 返还余额
            refund_sql = '''
                UPDATE money 
                SET balance = balance + %s, last_update = %s 
                WHERE user_id = %s
            '''
            refund_result = self.execute_sql(refund_sql, [amount, now, user_id], False)

            if refund_result != 1:
                return JsonResponse({'code': 500, 'msg': '订单取消成功，但退款失败，请联系管理员', 'data': None}, status=500)

            return JsonResponse({'code': 200, 'msg': '订单取消成功，金额已退回钱包', 'data': None}, status=200)

        except Exception as e:
            print('取消订单出错:', e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误', 'data': None}, status=500)
