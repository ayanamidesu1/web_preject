from base_api import BaseApi
from django.http import JsonResponse

class GetUserFollowStatus(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({
                    'code': 401,
                    'msg': '未登录',
                    'data': None
                },status=401)
            data=self.format_request(request)
            user_id=request.user.id
            target_id=data.get('target_id')
            if not target_id:
                return JsonResponse({
                    'code': 400,
                    'msg': '参数错误',
                    'data': None
                },status=400)
            sql='''
            select 1 from user_follow where user_id=%s and follow_user_id=%s
            '''
            if self.execute_sql(sql, (user_id,target_id)):
                return JsonResponse({
                    'code': 200,
                    'msg': '已关注',
                    'data': None,
                    'status':1
                },status=200)
            else:
                return JsonResponse({
                    'code': 200,
                    'msg': '未关注',
                    'data': None,
                    'status':0
                },status=200)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({
                'code': 500,
                'msg': '服务器错误',
                'data': None
            },status=500)