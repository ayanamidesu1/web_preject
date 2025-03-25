from django.db import connection, transaction
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import json
from datetime import datetime
from .log.log import Logger


class GetCommentList(View):
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

                limit = data.get('limit', 10)
                offset = data.get('offset', 0)
                sql = '''SELECT comment.*, users.userid, users.username, users.user_avatar
                         FROM comment 
                         LEFT JOIN users ON users.userid = comment.send_userid
                         ORDER BY date DESC 
                         LIMIT %s OFFSET %s'''
                cursor.execute(sql, [limit, offset])
                result = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]

                if result:
                    # 获取评论总数
                    count_sql = '''SELECT COUNT(*) FROM comment'''
                    cursor.execute(count_sql)
                    total = cursor.fetchone()[0]

                    # 获取每条评论关联的作品详情
                    for row in rows:
                        work_type = row.get("work_type", None)
                        work_id = row.get("work_id", None)
                        work_data = {}

                        if work_type == 'ill':
                            work_sql = """SELECT * FROM illustration_work WHERE Illustration_id = %s"""
                            cursor.execute(work_sql, [work_id])
                            result = cursor.fetchone()
                            if result:
                                columns = [desc[0] for desc in cursor.description]
                                work_data = dict(zip(columns, result))

                        elif work_type == 'comic':
                            work_sql = """SELECT * FROM comic WHERE id = %s"""
                            cursor.execute(work_sql, [work_id])
                            result = cursor.fetchone()
                            if result:
                                columns = [desc[0] for desc in cursor.description]
                                work_data = dict(zip(columns, result))

                        elif work_type == 'novel':
                            work_sql = """SELECT * FROM novel_work WHERE work_id = %s"""
                            cursor.execute(work_sql, [work_id])
                            result = cursor.fetchone()
                            if result:
                                columns = [desc[0] for desc in cursor.description]
                                work_data = dict(zip(columns, result))

                        # 将作品详情附加到对应的评论
                        row['work_data'] = work_data

                    return JsonResponse({
                        'status': 'success',
                        'message': '获取成功',
                        'data': {
                            'comment_list': rows,
                            'total': total
                        }
                    }, status=200)

        except json.JSONDecodeError:
            self.logger.error(f'请求数据格式错误：{self._request_path(request)}')
            return JsonResponse({'status': 'fail', 'message': '无效的JSON数据'}, status=400)

        except Exception as e:
            self.logger.error(f'服务器错误：{self._request_path(request)} - 错误详情：{str(e)}')
            return JsonResponse({'status': 'fail', 'message': '服务器错误'}, status=500)
