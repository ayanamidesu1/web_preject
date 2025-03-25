from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .log.log import Logger
from datetime import datetime
import json
from .authentication import Authentication


class GetIllList(View):
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
                with connection.cursor() as cursor:
                    sql = '''select account_permissions from users where userid=%s'''
                    cursor.execute(sql, (userid,))
                    account_permissions = cursor.fetchone()[0]
                    if account_permissions in ['1', '2', 1, 2]:
                        offset = data.get('offset')
                        limit = data.get('limit')
                        sql = ('select illustration_work.*,users.userid,users.user_avatar,users.username'
                               ' from illustration_work '
                               'left join users on users.userid=illustration_work.belong_to_user_id limit %s offset %s')
                        cursor.execute(sql, (limit, offset))
                        result = cursor.fetchall()
                        columns = [col[0] for col in cursor.description]
                        rows = [dict(zip(columns, row)) for row in result]
                        count_sql = '''select count(*) from illustration_work'''
                        cursor.execute(count_sql)
                        total = cursor.fetchone()[0]
                        return JsonResponse({'status': 'success', 'message': '请求成功',
                                             'data': {'work_list': rows, 'work_type': 'ill', 'total': total},
                                             'status_code': 200},
                                            status=200)
                return JsonResponse({'status': 'error', 'message': '权限不足', 'data': None, 'status_code': 403},
                                    status=403)
        except Exception as e:
            print('\n', e)
            self.logger.error(self._request_path(request) + '请求失败，错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '请求失败', 'data': None, 'status_code': 500},
                                status=500)
