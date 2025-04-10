from base_api import BaseApi
from django.http import JsonResponse


class getWalletInfo(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'}, status=401)
            sql = '''
            select * from money where user_id=%s 
            '''
            result = self.execute_sql(sql, (request.user.id,))
            if result:
                for i in result:
                    i.pop('pay_password', None)
                return JsonResponse({'code': 200, 'msg': '获取成功', 'data': result[0]}, status=200)
            return JsonResponse({'code': 200, 'msg': '获取成功', 'data': {}}, status=200)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
