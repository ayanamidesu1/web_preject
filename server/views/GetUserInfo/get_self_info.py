from base_api import  BaseApi
from django.http import JsonResponse

class GetSelfInfo(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '请先登录'},status=401)
            userid=request.user.id
            sql='''
            select * from users where userid=%s
            '''
            result=self.execute_sql(sql,params=(userid,))
            for i in result:
                i.pop('password',None)
            if result:
                return JsonResponse({'code': 200, 'msg': '获取成功', 'data': result[0]},status=200)
            else:
                return JsonResponse({'code': 404, 'msg': '用户不存在'},status=404)
        except Exception as e:
            print('获取自身自身信息失败\n',e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)