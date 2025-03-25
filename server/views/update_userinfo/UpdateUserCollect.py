from django.db import connection, transaction
from django.http import JsonResponse
from django.views import View
from ..log.log import Logger
from datetime import datetime
import json

class UpdateUserCollect(View):
    logger = Logger()

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', 'unknown')
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return f'{request_ip}在{now} 访问了 {request_path}'

    def get(self, request):
        self.logger.warning(self.request_path(request) + ' 非法GET请求：请求数据为：' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': '非法GET请求'}, status=403)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = getattr(request, 'userid', None)  # 只从中间件获取userid
            collect_id = data.get('collect_id')
            work_type = data.get('work_type')
            operate = data.get('operate')
            open_operate = data.get('open_operate', 1)  # 默认值为1

            if not userid:
                return JsonResponse({'status': 'error', 'message': '用户未登录'}, status=403)

            with transaction.atomic():
                with connection.cursor() as cursor:
                    if operate == 'delete':
                        cursor.execute(
                            'UPDATE user_collection_table SET is_collection=%s WHERE id=%s AND userid=%s AND type=%s',
                            [0, collect_id, userid, work_type]
                        )
                        if cursor.rowcount > 0:
                            return JsonResponse({'status': 'success', 'message': '取消收藏成功'})
                        else:
                            return JsonResponse({'status': 'error', 'message': '收藏项不存在'}, status=404)

                    elif operate == 'set_open':
                        if open_operate not in [0, 1, '0', '1']:
                            return JsonResponse({'status': 'error', 'message': '无效操作'}, status=400)
                        cursor.execute(
                            'UPDATE user_collection_table SET is_open=%s WHERE id=%s AND userid=%s AND type=%s',
                            [open_operate, collect_id, userid, work_type]
                        )
                        if cursor.rowcount > 0:
                            return JsonResponse({'status': 'success', 'message': '更新收藏状态成功'})
                        else:
                            return JsonResponse({'status': 'error', 'message': '收藏项不存在'}, status=404)

                    else:
                        return JsonResponse({'status': 'error', 'message': '无效操作'}, status=400)

        except json.JSONDecodeError as e:
            self.logger.warning(self.request_path(request) + ' 数据格式错误：请求数据为：' + str(request.body) + ' 错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '数据格式错误'}, status=400)
        except Exception as e:
            self.logger.error(self.request_path(request) + ' 错误信息：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
