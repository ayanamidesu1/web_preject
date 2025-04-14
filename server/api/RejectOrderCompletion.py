from django.http import JsonResponse
from base_api import BaseApi


class RejectOrderCompletion(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if self.check_user(request):
                return self.check_user(request)

            data = self.format_request(request)
            order_id = data.get('order_id')
            if not order_id:
                return JsonResponse({'code': 400, 'msg': '缺少参数'}, status=400)

            # 查询订单是否存在并属于当前用户
            check_sql = '''SELECT id FROM `order` WHERE id=%s AND user_id=%s'''
            result = self.execute_sql(check_sql, (order_id, request.user.id), True)

            if not result:
                return JsonResponse({'code': 403, 'msg': '订单不存在或无权限操作'}, status=403)

            # 设置订单为重新进行中
            update_sql = '''UPDATE `order` SET status=3 WHERE id=%s AND user_id=%s'''
            updated = self.execute_sql(update_sql, (order_id, request.user.id), False)

            if updated == 1:
                return JsonResponse({'code': 200, 'msg': '已拒绝订单完成状态'}, status=200)
            else:
                return JsonResponse({'code': 400, 'msg': '操作失败，订单状态未变更'}, status=400)

        except Exception as e:
            print("拒绝完成出错:", e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
