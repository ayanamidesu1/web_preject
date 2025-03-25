from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .log.log import Logger
from datetime import datetime
import json
from .authentication import Authentication


class UpdateComic(View):
    authentication = Authentication()
    logger = Logger()

    def _request_path(self, request):
        request_path = request.get_full_path()
        request_ip = request.META['REMOTE_ADDR']
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        return f'{request_ip}在{now}请求了{request_path}'

    def get(self, request):
        self.logger.warning(self._request_path(request) + '非法GET请求，请求数据为：' + str(request.GET))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = str(getattr(request, 'userid', None))
            is_authenticated = getattr(request, 'is_authenticated', None)

            if is_authenticated:
                # 查询用户权限
                sql = '''SELECT account_permissions FROM users WHERE userid=%s'''
                with connection.cursor() as cursor:
                    cursor.execute(sql, (userid,))
                    account_permissions = cursor.fetchone()[0]

                    # 判断是否有权限更新
                    if account_permissions in [1, 2, '1', '2']:
                        work_status = data.get('work_status', 2)  # 默认状态为 2 (待审核)
                        comic_id = data.get('work_id', None)

                        # 更新插画的审核状态
                        sql = '''UPDATE comic SET work_approved=%s WHERE id=%s'''
                        cursor.execute(sql, [work_status, comic_id])

                        # 判断更新操作是否成功
                        if cursor.rowcount > 0:
                            self.logger.info(self._request_path(request) + '更新成功')
                            return JsonResponse({'status': 'success', 'message': '更新成功'}, status=200)
                        else:
                            self.logger.error(self._request_path(request) + '更新失败，未找到匹配的记录')
                            return JsonResponse({'status': 'fail', 'message': '更新失败，未找到匹配的记录'}, status=500)

                    else:
                        self.logger.error(self._request_path(request) + '权限不足')
                        return JsonResponse({'status': 'fail', 'message': '权限不足'}, status=403)

            else:
                self.logger.error(self._request_path(request) + '未登录')
                return JsonResponse({'status': 'fail', 'message': '未登录'}, status=401)

        except Exception as e:
            self.logger.error(self._request_path(request) + '服务器错误：' + str(e))
            return JsonResponse({'status': 'fail', 'message': '服务器错误'}, status=500)
