from django.db import connection
from django.views import View
from django.http import JsonResponse
from ..log.log import Logger
from datetime import datetime
import json

class UpdateUserSelectWork(View):
    logger = Logger()

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', 'Unknown IP')
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        return f'{request_ip} 在 {now} 请求了 {request_path}'

    def get(self, request):
        self.logger.warning(self.request_path(request) + ' 非法 GET 请求：请求数据为：' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': '非法 GET 请求'}, status=403)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            select_work = data.get('select_work')
            userid = getattr(request, 'userid', None)  # 只从中间件获取userid

            if not userid:
                self.logger.warning(self.request_path(request) + ' 用户未登录：请求数据为：' + str(request.body))
                return JsonResponse({'status': 'error', 'message': '用户未登录'}, status=403)

            if not select_work:
                self.logger.warning(self.request_path(request) + ' 选择的作品为空：请求数据为：' + str(request.body))
                return JsonResponse({'status': 'error', 'message': '选择的作品不能为空'}, status=400)

            with connection.cursor() as cursor:
                # 转换 select_work 为 JSON 字符串
                select_work_json = json.dumps(select_work)
                cursor.execute('UPDATE users SET select_work = %s WHERE userid = %s', [select_work_json, userid])

                if cursor.rowcount >= 1:
                    self.logger.info(self.request_path(request) + ' 更新用户选择的作品成功：请求数据为：' + str(request.body))
                    return JsonResponse({'status': 'success', 'message': '更新用户选择的作品成功'})

                self.logger.warning(self.request_path(request) + ' 更新用户选择的作品失败：请求数据为：' + str(request.body))
                return JsonResponse({'status': 'error', 'message': '更新用户选择的作品失败'}, status=500)

        except json.JSONDecodeError as e:
            self.logger.error(self.request_path(request) + ' 请求体解析失败：' + str(e))
            return JsonResponse({'status': 'error', 'message': '请求体解析失败'}, status=400)
        except Exception as e:
            self.logger.error(self.request_path(request) + ' 服务器内部错误：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器内部错误'}, status=500)
