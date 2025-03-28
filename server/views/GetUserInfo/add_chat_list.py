from base_api import BaseApi
from django.http import JsonResponse

class AddChatList(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'},status=401)
            data=self.format_request(request)
            target_user_id=data.get('target_user_id')
            if not target_user_id:
                return JsonResponse({'code': 400, 'msg': '参数错误'},status=400)
            user_id=request.user.id
            if user_id==target_user_id:
                return JsonResponse({'code': 400, 'msg': '不能添加自己'},status=400)
            check_sql='''
            select 1 from chat_list where user_id=%s and target_user_id=%s
            '''
            if self.execute_sql(check_sql, (user_id, target_user_id), return_results=True):
                return JsonResponse({'code': 200, 'msg': '已存在'},status=200)
            sql='''
            insert into chat_list (user_id, target_user_id, join_time) values (%s,%s,%s)
            '''
            now=self.get_now()
            if self.execute_sql(sql, (user_id, target_user_id, now), return_results=False)>=1:
                return JsonResponse({'code': 200, 'msg': '添加成功'},status=200)
            else:
                return JsonResponse({'code': 400, 'msg': '添加失败'},status=400)

        except Exception as e:
            print(e)
            self.error_log(e,request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)