from base_api import BaseApi
from django.http import JsonResponse


class GetTargetFunc(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'}, status=401)
            user_id=request.user.id
            data=self.format_request(request)
            if not data:
                return JsonResponse({'code': 400, 'msg': '请求格式错误'}, status=400)
            target_user_id=data.get('target_user_id')
            limit=data.get('limit',10)
            offset=data.get('offset',0)
            if not target_user_id:
                return JsonResponse({'code': 400, 'msg': '请求格式错误'}, status=400)
            sql='''
            select * from commission_an_atricle where user_id=%s order by time limit %s offset %s
            '''
            results=self.execute_sql(sql, (target_user_id, limit, offset))
            total=self.execute_sql(
                'select count(*) as total from commission_an_atricle where user_id=%s',
                (target_user_id,))[0]['total']
            if results:
                return JsonResponse({'code': 200, 'msg': '获取成功', 'data': results, 'total': total}, status=200)
            return JsonResponse({'code': 200, 'msg': '获取成功', 'data': [],'total':0}, status=200)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)