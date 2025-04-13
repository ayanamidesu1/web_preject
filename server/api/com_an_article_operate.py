from base_api import BaseApi
from django.http import JsonResponse


class ComAnArticleOperate(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if self.check_user(request):
                return self.check_user(request)
            data = self.format_request(request)
            order_id = data.get('order_id')
            operate_type = data.get('operate_type')
            if not order_id or not operate_type:
                return JsonResponse({'code': 400, 'msg': '参数错误'}, status=400)
            user_id = request.user.id
            sql = '''
            update admin.order set status=%s where target_user_id=%s and id=%s
            '''
            if operate_type not in ['agree', 'refuse']:
                return JsonResponse({'code': 400, 'msg': '参数错误'}, status=400)
            if operate_type == 'agree':
                # 接受
                status = 2
            if operate_type == 'refuse':
                # 拒绝
                status = 5
            if self.execute_sql(sql, [status, user_id, order_id], False) != 1:
                return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
            return JsonResponse({'code': 200, 'msg': '操作成功'}, status=200)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
