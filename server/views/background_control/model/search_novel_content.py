from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import json
from datetime import datetime
from .log.log import Logger


class SearchNovelContent(View):
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
                self.logger.warning(f'未登录用户请求；{self._request_path(request)}')
                return JsonResponse({'status': 'fail', 'message': '未登录用户'}, status=401)

            # 检查用户权限
            with connection.cursor() as cursor:
                cursor.execute('SELECT account_permissions FROM users WHERE userid=%s', [userid])
                account_permissions = cursor.fetchone()

                if not account_permissions or account_permissions[0] not in ['1', '2', 1, 2]:
                    self.logger.warning(f'用户权限不足：{self._request_path(request)}')
                    return JsonResponse({'status': 'fail', 'message': '权限不足'}, status=403)

                # 校验work_id是否存在
                work_id = data.get('work_id')
                if work_id is None:
                    self.logger.warning(f'请求参数错误：{self._request_path(request)}')
                    return JsonResponse({'status': 'fail', 'message': '请求参数错误'}, status=400)

                # 构建基础 SQL 查询
                base_sql = '''
                    SELECT novel_content.*, users.userid, users.username, users.user_avatar, novel_work.work_cover,
                    novel_work.work_name, novel_work.is_vip_work
                    FROM novel_content
                    LEFT JOIN users ON users.userid = novel_content.belong_to_userid
                    LEFT JOIN novel_work ON novel_work.work_id = novel_content.belong_to_series_id
                    WHERE novel_content.belong_to_series_id = %s
                '''
                params = [work_id]

                # 处理搜索和状态过滤条件
                search_type = f"%{data.get('search_type', 'all')}%"
                work_status = data.get('work_status', 'all')
                limit = data.get('limit', 10)
                offset = data.get('offset', 0)

                if work_status != 'all':
                    base_sql += ' AND novel_content.chapter_approved = %s'
                    params.append(work_status)

                base_sql += ' AND (novel_content.id LIKE %s OR novel_content.title LIKE %s)'
                params.extend([search_type, search_type])

                # 排序和分页
                base_sql += ' ORDER BY novel_content.create_time DESC LIMIT %s OFFSET %s'
                params.extend([limit, offset])

                # 执行查询
                cursor.execute(base_sql, params)
                result = cursor.fetchall()

                # 构建返回结果
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]

                # 获取总数
                count_sql = 'SELECT COUNT(*) FROM novel_content WHERE novel_content.belong_to_series_id = %s'
                cursor.execute(count_sql, [work_id])
                total = cursor.fetchone()[0]

                return JsonResponse({
                    'status': 'success',
                    'message': '获取成功',
                    'data': {
                        'total': total,
                        'rows': rows
                    }
                }, status=200)

        except json.JSONDecodeError:
            self.logger.error(f'请求数据格式错误：{self._request_path(request)}')
            return JsonResponse({'status': 'fail', 'message': '无效的JSON数据'}, status=400)

        except Exception as e:
            self.logger.error(f'服务器错误：{self._request_path(request)} - 错误详情：{str(e)}')
            return JsonResponse({'status': 'fail', 'message': '服务器错误'}, status=500)
