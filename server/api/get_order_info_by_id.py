from django.http import JsonResponse
from base_api import BaseApi


class GetOrderInfoById(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if self.check_user(request):
                return self.check_user(request)
            data = self.format_request(request)
            order_id = data.get('order_id')
            if not order_id:
                return JsonResponse({'code': 400, 'msg': '缺少参数'}, status=400)
            sql = '''select * from admin.`order` where id=%s'''
            result = self.execute_sql(sql, [order_id])[0]
            if not result:
                return JsonResponse({'code': 400, 'msg': '订单不存在'}, status=400)
            if result.get('user_id') != request.user.id and result.get('target_user_id') != request.user.id:
                return JsonResponse({'code': 400, 'msg': '订单不存在，意外的访问'}, status=400)
            return JsonResponse({'code': 200, 'msg': '查询成功', 'data': result}, status=200)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
