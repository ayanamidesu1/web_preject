from django.db import connection, transaction
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import json
from datetime import datetime
from .log.log import Logger


class DeleteComment(View):
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

                comment_id_list = data.get('comment_id_list', [])

                if not isinstance(comment_id_list, list) or not comment_id_list:
                    self.logger.warning(
                        f'请求参数错误：{self._request_path(request)} - comment_id_list: {comment_id_list}')
                    return JsonResponse({'status': 'fail', 'message': '无效的参数'}, status=400)

                # 保持事务一致性
                with transaction.atomic():
                    sql = 'DELETE FROM comment WHERE comment_id IN %s'
                    cursor.execute(sql, [tuple(comment_id_list)])

                    # 记录日志
                    self.logger.info(f'用户{userid}删除了评论: {comment_id_list}')

                    if cursor.rowcount > 0:
                        return JsonResponse({'status': 'success', 'message': '删除成功'}, status=200)
                    else:
                        self.logger.warning(f'用户{userid}删除评论失败：comment_id_list: {comment_id_list}')
                        return JsonResponse({'status': 'fail', 'message': '删除失败'}, status=400)

        except json.JSONDecodeError:
            self.logger.error(f'请求数据格式错误：{self._request_path(request)}')
            return JsonResponse({'status': 'fail', 'message': '无效的JSON数据'}, status=400)

        except Exception as e:
            self.logger.error(f'服务器错误：{self._request_path(request)} - 错误详情：{str(e)}')
            return JsonResponse({'status': 'fail', 'message': '服务器错误'}, status=500)
