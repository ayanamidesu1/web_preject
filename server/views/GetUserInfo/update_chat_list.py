from base_api import BaseApi
from django.http import JsonResponse

class UpdateChatList(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            now=self.get_now()
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'},status=401)
            user_id=request.user.id
            data=self.format_request(request)
            target_id=data.get('target_id')
            if not target_id:
                return JsonResponse({'code': 400, 'msg': '参数错误'},status=400)
            update_sql='''
            update chat_list set join_time=%s where user_id=%s and target_user_id=%s
            '''
            if self.execute_sql(update_sql, (now, user_id, target_id), return_results=False)>=1:
                return JsonResponse({'code': 200, 'msg': '更新成功'})
            return JsonResponse({'code': 400, 'msg': '更新失败'},status=400)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)