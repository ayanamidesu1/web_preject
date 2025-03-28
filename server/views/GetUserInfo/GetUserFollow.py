from django.http import JsonResponse
from base_api import BaseApi


class GetUserFollow(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '请先登录'}, status=401)
            userid = request.user.id
            data=self.format_request(request)
            limit=data.get('limit',10)
            offset=data.get('offset',0)
            sql='''
            select count(*) as total from user_follow where user_id=%s
            '''
            fans_sql='''
            select count(*) as total from user_follow where follow_user_id=%s
            '''
            follow_list='''
            select * from user_follow where user_id=%s limit %s offset %s
            '''
            fans_list='''
            select * from user_follow where follow_user_id=%s limit %s offset %s
            '''
            follow_count=self.execute_sql(sql,params=(userid,))
            fans_count=self.execute_sql(fans_sql,params=(userid,))
            follow_list=self.execute_sql(follow_list,params=(userid,limit,offset))
            fans_list=self.execute_sql(fans_list,params=(userid,limit,offset))
            return JsonResponse({
                'code': 200,
                'msg': '获取成功',
                'data': {
                    'follow_list':follow_list,
                    'fans_list':fans_list,
                    'follow_count':follow_count[0]['total'],
                    'fans_count':fans_count[0]['total']
                }
            },status=200)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)