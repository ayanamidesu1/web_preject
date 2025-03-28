from base_api import BaseApi
from django.http import JsonResponse


class AddMsg(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({
                    'code': 401,
                    'msg': '未登录'
                }, status=401)
            data = self.format_request(request)
            target_user_id = data.get('target_user_id')
            user_id = request.user.id
            chat_type = data.get('chat_type', 'one_to_one')
            now = self.get_now()
            content = data.get('content')
            if not content:
                return JsonResponse({'code': 400, 'msg': '消息内容不能为空'}, status=400)
            group_id = data.get('group_id', None)
            if not target_user_id:
                return JsonResponse({
                    'code': 400,
                    'msg': '缺少参数'
                }, status=400)
            sql = '''
            insert into messages (sender_id, receiver_id, group_id, content, time, receiver_read_status, type) VALUES 
            (%s,%s,%s,%s,%s,%s,%s)
            '''
            if self.execute_sql(sql, [user_id, target_user_id, group_id, content, now, '未读', chat_type], False) >= 1:
                return JsonResponse({
                    'code': 200,
                    'msg': '发送成功'
                }, status=200)
            return JsonResponse({
                'code': 400,
                'msg': '发送失败'
            }, status=400)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({
                'code': 500,
                'msg': '服务器错误'
            }, status=500)
