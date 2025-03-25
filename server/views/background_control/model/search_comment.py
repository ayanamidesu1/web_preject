from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import json
from datetime import datetime
from .log.log import Logger


class SearchComment(View):
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

                # 读取分页和查询条件
                limit = data.get('limit', 10)
                offset = data.get('offset', 0)
                comment_id = data.get('comment_id', '')
                work_id = data.get('work_id', '')
                work_type = data.get('work_type', '')
                send_userid = data.get('send_userid', '')
                main_userid = data.get('main_userid', '')

                # 动态构建查询条件
                query_conditions = []
                query_params = []

                if comment_id:
                    query_conditions.append("comment.comment_id LIKE %s")
                    query_params.append(f'%{comment_id}%')

                if work_id:
                    query_conditions.append("comment.work_id LIKE %s")
                    query_params.append(f'%{work_id}%')

                if work_type and work_type != 'all':
                    query_conditions.append("comment.work_type LIKE %s")
                    query_params.append(f'%{work_type}%')

                if work_type == 'all':
                    query_conditions.append("comment.work_type IN ('ill', 'comic', 'novel')")

                if send_userid:
                    query_conditions.append("comment.send_userid LIKE %s")
                    query_params.append(f'%{send_userid}%')

                if main_userid:
                    query_conditions.append("comment.main_userid LIKE %s")
                    query_params.append(f'%{main_userid}%')

                # 构建SQL查询
                query_base = '''
                    SELECT comment.*, users.userid, users.username, users.user_avatar
                    FROM comment
                    LEFT JOIN users ON users.userid = comment.send_userid
                '''

                if query_conditions:
                    query_conditions_str = " WHERE " + " AND ".join(query_conditions)
                else:
                    query_conditions_str = ""

                query_order_limit = ' ORDER BY date DESC LIMIT %s OFFSET %s'
                query_sql = query_base + query_conditions_str + query_order_limit
                query_params.extend([limit, offset])

                # 执行查询
                cursor.execute(query_sql, query_params)
                result = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]

                # 统计总数
                count_sql = 'SELECT COUNT(*) FROM comment' + query_conditions_str
                cursor.execute(count_sql, query_params[:-2])  # 去掉分页参数
                total = cursor.fetchone()[0]

                # 获取每条评论关联的作品详情
                for row in rows:
                    work_type = row.get("work_type", None)
                    work_id = row.get("work_id", None)
                    work_data = {}

                    if work_type == 'ill':
                        work_sql = """SELECT * FROM illustration_work WHERE Illustration_id = %s"""
                        cursor.execute(work_sql, [work_id])
                        work_result = cursor.fetchone()
                        if work_result:
                            work_columns = [desc[0] for desc in cursor.description]
                            work_data = dict(zip(work_columns, work_result))

                    elif work_type == 'comic':
                        work_sql = """SELECT * FROM comic WHERE id = %s"""
                        cursor.execute(work_sql, [work_id])
                        work_result = cursor.fetchone()
                        if work_result:
                            work_columns = [desc[0] for desc in cursor.description]
                            work_data = dict(zip(work_columns, work_result))

                    elif work_type == 'novel':
                        work_sql = """SELECT * FROM novel_work WHERE work_id = %s"""
                        cursor.execute(work_sql, [work_id])
                        work_result = cursor.fetchone()
                        if work_result:
                            work_columns = [desc[0] for desc in cursor.description]
                            work_data = dict(zip(work_columns, work_result))

                    # 将作品详情附加到对应的评论
                    row['work_data'] = work_data

                if result:
                    return JsonResponse({
                        'status': 'success',
                        'message': '查询成功',
                        'data': {
                            'rows': rows,
                            'total': total
                        }
                    }, status=200)
                else:
                    return JsonResponse({
                        'status': 'success',
                        'message': '没有找到匹配的结果',
                        'data': {
                            'rows': [],
                            'total': 0
                        }
                    }, status=200)

        except json.JSONDecodeError:
            self.logger.error(f'请求数据格式错误：{self._request_path(request)}')
            return JsonResponse({'status': 'fail', 'message': '无效的JSON数据'}, status=400)

        except Exception as e:
            self.logger.error(f'服务器错误：{self._request_path(request)} - 错误详情：{str(e)}')
            return JsonResponse({'status': 'fail', 'message': '服务器错误'}, status=500)
