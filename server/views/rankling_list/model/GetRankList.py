from django.db import connection
from django.views import View
from django.http import JsonResponse
from datetime import datetime, timedelta
from ..log.log import Logger
import json
from django.shortcuts import render

class GetRankList(View):
    logger = Logger()

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', 'unknown IP')
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        return f'{request_ip}在{now}访问了{request_path}'

    def get(self, request):
        self.logger.warning(self.request_path(request) + '非法GET请求：请求数据为：' + str(request.GET))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        last_day = (datetime.now() - timedelta(days=10086)).strftime('%Y-%m-%dT%H:%M:%S')

        try:
            data = json.loads(request.body.decode('utf-8'))
            work_type = data.get('work_type', 'ill')

            # SQL 查询
            sql_queries = {
                'watch': '''SELECT * FROM user_watch_table WHERE time < %s AND time > %s LIMIT 50''',
                'like': '''SELECT * FROM user_like_table WHERE time < %s AND time > %s LIMIT 50''',
                'collect': '''SELECT * FROM user_collection_table WHERE time < %s AND time > %s LIMIT 50'''
            }

            info_sql_map = {
                'ill': '''SELECT illustration_work.*, users.username AS author_username, users.userid AS author_userid,
                             users.user_avatar AS author_avatar
                          FROM illustration_work 
                          LEFT JOIN users ON users.userid = illustration_work.belong_to_user_id 
                          WHERE Illustration_id = %s and work_approved=1''',
                'comic': '''SELECT comic.*, users.username AS author_username, users.userid AS author_userid,
                             users.user_avatar AS author_avatar 
                            FROM comic 
                            LEFT JOIN users ON users.userid = comic.belong_to_userid 
                            WHERE comic.id = %s and work_approved=1''',
                'novel': '''SELECT novel_work.*, users.username AS author_username, users.userid AS author_userid,
                             users.user_avatar AS author_avatar
                            FROM novel_work 
                            LEFT JOIN users ON users.userid = novel_work.belong_to_userid 
                            WHERE work_id = %s and work_approved=1'''
            }

            weights = {
                'watch': 1,
                'like': 2,
                'collect': 3
            }

            work_list = []

            with connection.cursor() as cursor:
                for action, query in sql_queries.items():
                    cursor.execute(query, [now, last_day])
                    data_dict = self.format_dict(cursor.description, cursor.fetchall())
                    weight = weights[action]
                    for item in data_dict:
                        if item['type'] == work_type:
                            item['weight'] = weight
                            work_list.append(item)

            # 去重
            seen = set()
            unique_work_list = []
            for item in work_list:
                if item['workid'] not in seen:
                    seen.add(item['workid'])
                    unique_work_list.append(item)

            # 排序
            unique_work_list.sort(key=lambda x: x['weight'], reverse=True)

            # 获取作品详细信息
            detailed_work_info = self.get_detailed_work_info(unique_work_list, info_sql_map)

            return JsonResponse({'status': 'success', 'data': detailed_work_info})

        except json.JSONDecodeError as e:
            self.logger.error(self.request_path(request) + '请求数据格式错误：' + str(e))
            return JsonResponse({'status': 'error', 'message': '请求数据格式错误'}, status=400)
        except Exception as e:
            self.logger.error(self.request_path(request) + '服务器内部错误：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器内部错误'}, status=500)

    def format_dict(self, description, rows):
        return [
            dict(zip([col[0] for col in description], row))
            for row in rows
        ]

    def get_detailed_work_info(self, work_list, info_sql_map):
        detailed_info = []

        with connection.cursor() as cursor:
            for item in work_list:
                sql = info_sql_map.get(item['type'])
                if sql:
                    cursor.execute(sql, [item['workid']])
                    details = self.format_dict(cursor.description, cursor.fetchall())
                    if details:
                        work_info = details[0]
                        # 删除敏感字段
                        work_info.pop('password', None)
                        work_info.pop('token', None)
                        # 组装返回的数据
                        work_data = {
                            'work_id': item['workid'],
                            'work_type': item['type'],
                            'weight': item['weight'],
                            'work_info': {key: value for key, value in work_info.items() if key not in ['author_username', 'author_userid', 'author_avatar']},
                            'author_info': {
                                'author_id': work_info.get('author_userid'),
                                'author_username': work_info.get('author_username'),
                                'author_avatar': work_info.get('author_avatar')
                            }
                        }
                        detailed_info.append(work_data)

        return detailed_info
