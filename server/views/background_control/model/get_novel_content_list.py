from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import json
from datetime import datetime
from .log.log import Logger


class GetNovelContentList(View):
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
                return JsonResponse({'status': 'fail', 'message': '用户未登录'}, status=401)

            # 检查用户权限
            with connection.cursor() as cursor:
                cursor.execute('SELECT account_permissions FROM users WHERE userid=%s', [userid])
                account_permissions = cursor.fetchone()

                if not account_permissions or account_permissions[0] not in [1, 2, '1', '2']:
                    self.logger.warning(f'用户权限不足：{self._request_path(request)}')
                    return JsonResponse({'status': 'fail', 'message': '权限不足'}, status=403)

                # 查询小说内容列表
                work_id = data.get('work_id')
                if not work_id:
                    return JsonResponse({'status': 'fail', 'message': '作品ID缺失'}, status=400)

                limit = data.get('limit', 10)
                offset = data.get('offset', 0)

                # 分页查询小说内容
                query_sql = '''
                SELECT novel_content.*, users.userid, users.username, users.user_avatar, novel_work.work_cover,
                novel_work.work_name, novel_work.is_vip_work
                FROM novel_content
                LEFT JOIN users ON users.userid = novel_content.belong_to_userid
                LEFT JOIN novel_work ON novel_work.work_id = novel_content.belong_to_series_id
                WHERE novel_content.belong_to_series_id = %s
                ORDER BY novel_content.create_time DESC
                LIMIT %s OFFSET %s
                '''
                cursor.execute(query_sql, [work_id, limit, offset])
                result = cursor.fetchall()

                if result:
                    columns = [col[0] for col in cursor.description]
                    rows = [dict(zip(columns, row)) for row in result]
                    # 计算小说内容的总字数，不受分页限制
                    word_count_sql = '''
                                    SELECT SUM(CHAR_LENGTH(novel_content.content))
                                    FROM novel_content
                                    WHERE novel_content.belong_to_series_id = %s
                                    '''
                    cursor.execute(word_count_sql, [work_id])
                    total_word_count = cursor.fetchone()[0] or 0  # 防止空值返回None

                    # 计算总条数
                    count_sql = 'SELECT COUNT(*) FROM novel_content WHERE belong_to_series_id=%s'
                    cursor.execute(count_sql, [work_id])
                    total = cursor.fetchone()[0]

                    return JsonResponse({
                        'status': 'success',
                        'data': {
                            'work_list': rows,
                            'total': total,
                            'total_word_count': total_word_count  # 总字数统计
                        }
                    }, status=200)
                else:
                    return JsonResponse({'status': 'fail', 'message': '没有找到相关作品'}, status=404)

        except json.JSONDecodeError:
            self.logger.error(f'请求数据格式错误：{self._request_path(request)}')
            return JsonResponse({'status': 'fail', 'message': '无效的JSON数据'}, status=400)

        except Exception as e:
            self.logger.error(f'服务器错误：{self._request_path(request)} - 错误详情：{str(e)}')
            return JsonResponse({'status': 'fail', 'message': '服务器错误'}, status=500)
