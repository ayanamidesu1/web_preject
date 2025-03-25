from django.db import connection
from django.http import JsonResponse
from django.views import View
from ..log.log import Logger
from datetime import datetime, timedelta
import json
from django.shortcuts import render


class GetAllWorkData(View):
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
        try:
            now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            data = json.loads(request.body.decode('utf-8'))
            ago_days = data.get('ago_date')
            userid = getattr(request, 'userid', None)  # 从中间件获取userid
            print(data)

            if not userid:
                self.logger.warning(self.request_path(request) + '用户ID为空')
                return JsonResponse({'status': 'error', 'message': '用户ID为空'}, status=401)

            if not ago_days:
                ago_days = 7

            target_date = (datetime.now() - timedelta(days=int(ago_days))).strftime('%Y-%m-%dT%H:%M:%S')
            history_date = datetime(1900, 1, 1).strftime('%Y-%m-%dT%H:%M:%S')

            with connection.cursor() as cursor:
                # 获取用户所有作品 ID
                sql_dict = {
                    'ill': 'SELECT Illustration_id AS work_id FROM illustration_work WHERE belong_to_user_id=%s',
                    'comic': 'SELECT id AS work_id FROM comic WHERE belong_to_userid=%s',
                    'novel': 'SELECT work_id AS work_id FROM novel_work WHERE belong_to_userid=%s'
                }

                work_ids = {'ill': [], 'comic': [], 'novel': []}
                for work_type, sql in sql_dict.items():
                    cursor.execute(sql, [userid])  # 直接使用userid
                    work_ids[work_type] = [row[0] for row in cursor.fetchall()]

                # 统计交互数据
                interaction_sql_dict = {
                    'watch': 'SELECT COUNT(*) FROM user_watch_table WHERE workid=%s AND type=%s AND time>%s AND time<%s',
                    'like': 'SELECT COUNT(*) FROM user_like_table WHERE workid=%s AND type=%s AND time>%s AND time<%s',
                    'collect': 'SELECT COUNT(*) FROM user_collection_table WHERE workid=%s AND type=%s AND time>%s AND time<%s'
                }

                def count_interactions(work_ids, work_type, start_date, end_date):
                    counts = {'watch': 0, 'like': 0, 'collect': 0}
                    for work_id in work_ids:
                        for interaction_type, sql in interaction_sql_dict.items():
                            cursor.execute(sql, [work_id, work_type, start_date, end_date])
                            counts[interaction_type] += cursor.fetchone()[0]
                    return counts

                target_data = {'ill': {}, 'comic': {}, 'novel': {}}
                history_data = {'ill': {}, 'comic': {}, 'novel': {}}

                for work_type in work_ids:
                    target_counts = count_interactions(work_ids[work_type], work_type, target_date, now)
                    history_counts = count_interactions(work_ids[work_type], work_type, history_date, target_date)
                    target_data[work_type] = target_counts
                    history_data[work_type] = history_counts

                return JsonResponse({
                    'status': 'success',
                    'data': {
                        'target_data': target_data,
                        'history_data': history_data
                    }
                }, status=200)

        except ValueError as e:
            self.logger.error(self.request_path(request) + '参数格式错误：' + str(e))
            return JsonResponse({'status': 'error', 'message': '参数格式错误'}, status=400)
        except Exception as e:
            self.logger.error(self.request_path(request) + '服务器内部错误：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器内部错误'}, status=500)
