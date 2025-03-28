from base_api import  BaseApi
from django.http import JsonResponse

class GetChatList(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'},status=401)
            data=self.format_request(request)
            limit=data.get('limit',10)
            offset=data.get('offset',0)
            get_chat_list='''
            select chat_list.*,users.userid as userid,users.user_avatar as avatar,users.username from chat_list
            left join users on users.userid=chat_list.target_user_id
             where chat_list.user_id=%s order by join_time limit %s offset %s
            '''
            total_sql='''
            select count(*) as total from chat_list where user_id=%s
            '''
            total=self.execute_sql(total_sql,(request.user.id,))
            result=self.execute_sql(get_chat_list,(request.user.id,limit,offset))
            return JsonResponse({'code': 200, 'msg': '获取成功','data':result,'total':total[0]['total']}
                                ,status=200)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)