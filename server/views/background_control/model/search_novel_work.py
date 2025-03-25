from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import json
from datetime import datetime
from .log.log import Logger


class SearchNovelWork(View):
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

                # 查询条件和参数构建
                limit = data.get('limit', 10)
                offset = data.get('offset', 0)
                work_status = data.get('work_status', 'all')
                search_type = data.get('search_type', '*')

                # 构建 SQL 查询
                base_sql = '''
                    SELECT novel_work.*, users.userid, users.user_avatar, users.username,
                    sum(char_length(novel_content.content)) as "novel_word_count"
                    FROM novel_work
                    LEFT JOIN users ON users.userid = novel_work.belong_to_userid 
                    left join novel_content on novel_content.belong_to_series_id=novel_work.work_id
                    WHERE (novel_work.work_name LIKE %s OR novel_work.work_id LIKE %s OR novel_work.category LIKE %s)
                '''
                params = [f'%{search_type}%', f'%{search_type}%', f'%{search_type}%']

                # 如果有指定作品状态，则添加状态过滤
                if work_status != 'all':
                    base_sql += ' AND novel_work.work_approved = %s'
                    params.append(work_status)

                # 限制和偏移量
                base_sql += 'group by novel_work.work_id ORDER BY novel_work.work_create_time DESC LIMIT %s OFFSET %s'
                params.extend([limit, offset])

                # 执行查询
                cursor.execute(base_sql, params)
                result = cursor.fetchall()
                # 构建返回数据
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]

                # 获取总条数
                count_sql = 'SELECT COUNT(*) FROM novel_work'
                cursor.execute(count_sql)
                total = cursor.fetchone()[0]

                return JsonResponse({
                    'status': 'success',
                    'data': {
                        'work_list': rows,
                        'total': total
                    }
                }, status=200)

        except json.JSONDecodeError:
            self.logger.error(f'请求数据格式错误：{self._request_path(request)}')
            return JsonResponse({'status': 'fail', 'message': '无效的JSON数据'}, status=400)

        except Exception as e:
            print('\n',e)
            self.logger.error(f'服务器错误：{self._request_path(request)} - 错误详情：{str(e)}')
            return JsonResponse({'status': 'fail', 'message': '服务器错误'}, status=500)
