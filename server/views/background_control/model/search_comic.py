from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .log.log import Logger
from datetime import datetime
import json
from .authentication import Authentication


class SearchComic(View):
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
                    # 获取用户权限
                    sql = '''SELECT account_permissions FROM users WHERE userid=%s'''
                    cursor.execute(sql, (userid,))
                    account_permissions = cursor.fetchone()[0]

                    if account_permissions in ['1', '2', 1, 2]:
                        offset = int(data.get('offset', 0))
                        limit = int(data.get('limit', 10))
                        search_key = data.get('search_key', '').strip()
                        work_status = data.get('work_status', 'all')

                        # 模糊查询关键字处理
                        search_key = f"%{search_key}%"

                        # 初始化查询条件
                        filters = []
                        params = []

                        # 插入模糊搜索条件
                        filters.append(
                            "(comic.id LIKE %s OR comic.work_name LIKE %s OR "
                            "users.username LIKE %s OR users.userid LIKE %s)")
                        params.extend([search_key, search_key, search_key, search_key])

                        # 插入状态过滤条件
                        if work_status != 'all':
                            filters.append("comic.work_approved = %s")
                            params.append(work_status)

                        # 拼接查询语句
                        sql_query = f'''
                            SELECT comic.*, users.userid, users.user_avatar, users.username
                            FROM comic
                            LEFT JOIN users ON users.userid = comic.belong_to_userid
                            WHERE {" AND ".join(filters)}
                            LIMIT %s OFFSET %s
                        '''
                        params.extend([limit, offset])

                        cursor.execute(sql_query, params)
                        result = cursor.fetchall()

                        # 获取列名
                        columns = [col[0] for col in cursor.description]
                        rows = [dict(zip(columns, row)) for row in result]

                        # 查询总数
                        count_sql = f'''
                            SELECT COUNT(*) 
                            FROM comic
                            LEFT JOIN users ON users.userid = comic.belong_to_userid
                            WHERE {" AND ".join(filters)}
                        '''
                        cursor.execute(count_sql, params[:-2])  # 去掉 limit 和 offset
                        total = cursor.fetchone()[0]

                        return JsonResponse({
                            'status': 'success',
                            'message': '请求成功',
                            'data': {'work_list': rows, 'work_type': 'ill', 'total': total},
                            'status_code': 200
                        }, status=200)

                    return JsonResponse({
                        'status': 'error',
                        'message': '权限不足',
                        'data': None,
                        'status_code': 403
                    }, status=403)

        except Exception as e:
            print('\n', e)
            self.logger.error(self._request_path(request) + '请求失败，错误信息为：' + str(e))
            return JsonResponse({
                'status': 'error',
                'message': '请求失败',
                'data': None,
                'status_code': 500
            }, status=500)

