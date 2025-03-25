from django.db import connection
from django.views import View
from django.http import JsonResponse
from ..log.log import Logger
from datetime import datetime
import json


class DeleteUserBack(View):
    logger = Logger()

    def request_path(self, request):
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', 'unknown')
        return f'{request_ip}在{now}访问了{request_path}'

    def get(self, request):
        self.logger.warning(self.request_path(request) + ' 非法GET请求')
        return JsonResponse({'status': 'error', 'message': '非法GET请求'}, status=403)

    def post(self, request, *args, **kwargs):
        try:
            # 解析请求数据
            data = json.loads(request.body.decode('utf-8'))
            userid = getattr(request, 'userid', None)

            if not userid:
                self.logger.warning(self.request_path(request) + ' 请求失败，用户ID缺失')
                return JsonResponse({'status': 'error', 'message': '用户ID缺失'}, status=400)

            # 直接使用 `userid` 进行操作
            with connection.cursor() as cursor:
                cursor.execute('SELECT userid FROM users WHERE userid=%s', [userid])
                user_result = cursor.fetchone()

                if user_result:
                    # 更新用户的背景图片
                    new_image_filename = '20240525174916_f4f4acc7280f4eabb9fc1712929c3ccc.png'
                    cursor.execute('UPDATE users SET user_back_img=%s WHERE userid=%s',
                                   [new_image_filename, userid])
                    if cursor.rowcount >= 1:
                        self.logger.info(self.request_path(request) + ' 请求成功')
                        return JsonResponse({'status': 'success', 'message': '请求成功'}, status=200)
                    else:
                        self.logger.warning(self.request_path(request) + ' 更新失败，用户不存在')
                        return JsonResponse({'status': 'error', 'message': '用户不存在'}, status=400)
                else:
                    self.logger.warning(self.request_path(request) + ' 请求失败，用户不存在')
                    return JsonResponse({'status': 'error', 'message': '用户不存在'}, status=400)

        except json.JSONDecodeError as e:
            self.logger.error(self.request_path(request) + ' 数据解析失败，错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '数据解析失败'}, status=400)
        except Exception as e:
            self.logger.error(self.request_path(request) + ' 服务器错误，错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
