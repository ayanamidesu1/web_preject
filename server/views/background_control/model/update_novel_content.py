from django.db import connection, transaction
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import json
from datetime import datetime
from .log.log import Logger


class UpdateNovelContent(View):
    logger = Logger()

    def _request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        content = request.body.decode('utf-8')
        return f'{request_ip}在{now}请求了{request_path}, 请求内容为：{content}'

    def get(self, request):
        self.logger.warning(f'非法GET请求；{self._request_path(request)}')
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = str(getattr(request, 'userid', None))
            is_authenticated = getattr(request, 'is_authenticated', None)

            if not is_authenticated:
                self.logger.warning(f'未登录用户尝试访问：{self._request_path(request)}')
                return JsonResponse({'status': 'fail', 'message': '未登录'}, status=401)

            # 检查用户权限
            with connection.cursor() as cursor:
                cursor.execute('SELECT account_permissions FROM users WHERE userid=%s', [userid])
                account_permissions = cursor.fetchone()

                if not account_permissions or account_permissions[0] not in ['1', '2', 1, 2]:
                    self.logger.warning(f'用户权限不足：{self._request_path(request)}')
                    return JsonResponse({'status': 'fail', 'message': '权限不足'}, status=403)

                work_id = data.get('work_id', None)
                if not work_id:
                    self.logger.warning(f'缺少work_id参数：{self._request_path(request)}')
                    return JsonResponse({'status': 'fail', 'message': '缺少参数'}, status=400)

                work_status = data.get('work_status', 2)
                chapter_ids = data.get('chapter_id', [])
                if not chapter_ids or not isinstance(chapter_ids, list):
                    self.logger.warning(f'缺少chapter_id参数或格式错误：{self._request_path(request)}')
                    return JsonResponse({'status': 'fail', 'message': '缺少参数或格式错误'}, status=400)

                # 开始事务
                with transaction.atomic():
                    # 使用IN语句更新多个chapter_id
                    sql = ('UPDATE novel_content SET novel_content.chapter_approved = %s '
                           'WHERE novel_content.belong_to_series_id = %s AND id IN %s')
                    # 将chapter_ids转换为元组，以便用于SQL的IN子句
                    cursor.execute(sql, [work_status, work_id, tuple(chapter_ids)])

                    if cursor.rowcount >= 1:
                        return JsonResponse({'status': 'success', 'message': '更新成功'}, status=200)
                    else:
                        self.logger.error(f'更新失败，work_id: {work_id}, {self._request_path(request)}')
                        return JsonResponse({'status': 'fail', 'message': '更新失败'}, status=500)

        except json.JSONDecodeError:
            self.logger.error(f'请求数据格式错误：{self._request_path(request)}')
            return JsonResponse({'status': 'fail', 'message': '无效的JSON数据'}, status=400)

        except Exception as e:
            self.logger.error(f'服务器错误：{self._request_path(request)} - 错误详情：{str(e)}')
            return JsonResponse({'status': 'fail', 'message': '服务器错误'}, status=500)
