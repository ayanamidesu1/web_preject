from base_api import BaseApi
from django.http import JsonResponse


class GetUserFuncList(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            data = self.format_request(request)
            target_user_id = data.get('target_user_id', None)
            limit = data.get('limit', 0)
            offset = data.get('offset', 0)
            if target_user_id is None:
                return JsonResponse({'code': 400, 'msg': '缺少参数', 'data': []}, status=400)
            sql = '''select * from commission_an_atricle where user_id=%s limit %s offset %s'''
            total_sql = '''select count(*) as total from commission_an_atricle where user_id=%s'''
            result = self.execute_sql(sql, (target_user_id, limit, offset))
            total = self.execute_sql(total_sql, (target_user_id,))[0].get('total', 0)
            if result is None:
                return JsonResponse({'code': 200, 'msg': '成功，用户未开通接稿', 'data': [], 'total': total}, status=200)
            return JsonResponse({'code': 200, 'msg': '成功', 'data': result, 'total': total}, status=200)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器内部错误', 'data': []}, status=500)
