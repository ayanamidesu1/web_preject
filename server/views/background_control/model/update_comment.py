from django.db import connection, transaction
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import json
from datetime import datetime
from .log.log import Logger


class UpdateComment(View):
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

            comment_id = data.get('comment_id')
            content = data.get('content')

            if not comment_id or not content:
                return JsonResponse({'status': 'fail', 'message': '参数错误'}, status=400)

            # 检查用户权限
            with connection.cursor() as cursor:
                cursor.execute('SELECT account_permissions FROM users WHERE userid=%s', [userid])
                account_permissions = cursor.fetchone()

                if not account_permissions or account_permissions[0] not in ['1', '2', 1, 2]:
                    self.logger.warning(f'用户权限不足：{self._request_path(request)}')
                    return JsonResponse({'status': 'fail', 'message': '权限不足'}, status=403)

                # 开始事务
                with transaction.atomic():
                    # 更新评论
                    sql = '''UPDATE comment SET content=%s WHERE comment_id=%s'''
                    cursor.execute(sql, [content, comment_id])

                    if cursor.rowcount != 1:
                        # 如果修改行数不为1，则回滚事务并返回错误
                        transaction.set_rollback(True)
                        self.logger.warning(f'修改失败：{self._request_path(request)}')
                        return JsonResponse({'status': 'fail', 'message': '修改失败'}, status=400)

                # 如果成功修改，提交事务
                return JsonResponse({'status': 'success', 'message': '修改成功'})

        except Exception as e:
            self.logger.error(f"{self._request_path(request)} 发生错误：{str(e)}")
            return JsonResponse({
                'status': 'fail',
                'message': 'server_error'
            }, status=500)
