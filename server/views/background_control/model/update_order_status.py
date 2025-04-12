from django.http import JsonResponse
from base_api import BaseApi


class UpdateOrderStatus(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if self.check_admin(request):
                return self.check_admin(request)
            data = self.format_request(request)
            order_id = int(data.get('order_id'))
            status = int(data.get('status'))
            if not order_id or not status:
                return JsonResponse({'code': 400, 'msg': '参数错误'}, status=400)
            # 订单状态，0取消，1完成，2进行中，3收到但未开始，4待确认，5已拒绝
            status_list = [0, 1, 2, 3, 4, 5]
            if status not in status_list:
                return JsonResponse({'code': 400, 'msg': '参数错误'}, status=400)
            sql = '''
            update admin.order set status=%s where id=%s
            '''
            if self.execute_sql(sql, (status, order_id), return_results=False) == 1:
                return JsonResponse({'code': 200, 'msg': '修改成功'}, status=200)
            return JsonResponse({'code': 400, 'msg': '修改失败'}, status=400)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
