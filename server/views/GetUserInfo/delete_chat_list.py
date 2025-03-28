from base_api import BaseApi
from django.http import JsonResponse

class DeleteChatList(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'},status=401)
            data=self.format_request(request)
            if not data:
                return JsonResponse({'code': 400, 'msg': '请求格式错误'},status=400)
            target_id=data.get('target_id')
            if not target_id:
                return JsonResponse({'code': 400, 'msg': '请求格式错误'},status=400)
            user_id=request.user.id
            sql='''
            delete from chat_list where user_id=%s and target_user_id=%s
            '''
            if self.execute_sql(sql, (user_id,target_id), return_results=False)>=1:
                return JsonResponse({'code': 200, 'msg': '删除成功'},status=200)
            else:
                return JsonResponse({'code': 400, 'msg': '删除失败'},status=400)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)