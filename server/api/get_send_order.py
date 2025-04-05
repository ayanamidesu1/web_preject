from base_api import BaseApi
from django.http import JsonResponse

class GetSendOrder(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'},status=401)
            user_id = request.user.id
            data=self.format_request(request)
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)
            sql='''
            select * from order where user_id=%s order by time limit %s offset %s
            '''
            result=self.execute_sql(sql, (user_id, limit, offset))
            total=self.execute_sql('''
            select count(*) as total from order where user_id=%s
            ''', (user_id,))[0]['total']
            if result:
                return JsonResponse({'code': 200, 'msg': '获取成功', 'data': result, 'total': total},status=200)
            else:
                return JsonResponse({'code':200,'msg':'获取成功','data':[],'total':0},status=200)
        except Exception as e:
            print(e)
            self.error_log(e,request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)