from base_api import BaseApi
from django.http import JsonResponse

class GetFuncList(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            data=self.format_request(request)
            user_id=data.get('user_id')
            if not user_id:
                user_id=request.user.id
                if not user_id:
                    return JsonResponse({'code': 400, 'msg': '缺少参数'},status=400)
            limit=data.get('limit',10)
            offset=data.get('offset',0)
            sql='''
            select * from admin.commission_an_atricle where user_id=%s order by time desc limit %s offset %s
            '''
            result=self.execute_sql(sql,(user_id,limit,offset))
            total=self.execute_sql('''
            select count(*) as total from admin.commission_an_atricle where user_id=%s
            ''',(user_id,))[0]['total']
            if not result:
                return JsonResponse({'code': 200, 'msg': '获取成功','data':[],'total':0},status=200)
            return JsonResponse({'code': 200, 'msg': '获取成功','data':result,'total':total},status=200)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)