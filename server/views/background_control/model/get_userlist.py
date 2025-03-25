from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .log.log import Logger
from datetime import datetime
import json
from .authentication import Authentication


class GetUserList(View):
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
                with connection.cursor() as cursor:
                    sql = '''select account_permissions from users where userid=%s'''
                    cursor.execute(sql, (userid,))
                    account_permissions = cursor.fetchone()[0]
                if account_permissions in ['1', '2', 1, 2]:
                    offset = data.get('offset',0)
                    limit = data.get('limit',10)
                    sql = '''select * from users limit %s offset %s'''
                    count_sql='''select count(*) from users'''
                    cursor = connection.cursor()
                    cursor.execute(sql,[limit,offset])
                    columns = [col[0] for col in cursor.description]
                    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    cursor.execute(count_sql)
                    all_user_count = cursor.fetchone()[0]
                    return JsonResponse({
                        'status': 'success',
                        'message': '获取用户列表成功！',
                        'status_code': 200,
                        'data': {'user_list':rows},
                        'total':all_user_count
                    },status=200)
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': '用户权限不足！',
                        'status_code': 403
                    },status=403)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': '用户未登录！',
                    'status_code': 401
                },status=401)
        except Exception as e:
            print(e)
            self.logger.error(f'{self._request_path(request)}请求失败，错误信息为：{str(e)}')
            return_data = JsonResponse({'status': 'error', 'message': '服务器错误！'})
            return return_data

