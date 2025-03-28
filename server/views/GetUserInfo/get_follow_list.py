from base_api import BaseApi
from django.http import JsonResponse

class GetFollowList(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'},status=401)
            user_id = request.user.id
            data=self.format_request(request)
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)
            sql='''
            select * from user_follow where user_id=%s limit %s offset %s
            '''
            result=self.execute_sql(sql, (user_id, limit, offset))
            return JsonResponse({'code': 200, 'msg': '获取成功', 'data': result},status=200)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)