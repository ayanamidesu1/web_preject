from django.db import connection
from django.views import View
from django.http import JsonResponse
from datetime import datetime
from ..log.log import Logger
import json


class GetNovelList(View):
    logger = Logger()

    def request_path(self, request):
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', 'unknown')
        return f'请求IP：{request_ip}，请求地址：{request_path}，时间：{now}'

    def get(self, request):
        self.logger.info(self.request_path(request) + '非法GET访问，访问数据为：' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': '非法GET访问'}, status=403)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            userid = getattr(request, 'userid', None)
            work_id = data.get('work_id')

            if not userid:
                self.logger.warning(self.request_path(request) + '数据获取失败，失败原因：用户id为空')
                return JsonResponse({'status': 'error', 'message': '用户id为空'}, status=400)

            with connection.cursor() as cursor:
                sql = '''SELECT novel_work.work_name, novel_work.work_cover, novel_work.is_vip_work, 
                        novel_work.work_status, novel_content.*, novel_work.brief_introduction, novel_work.work_id
                        FROM novel_content 
                        JOIN novel_work ON novel_work.work_id = novel_content.belong_to_series_id 
                        WHERE belong_to_series_id = %s and work_approved=1 and chapter_approved=1 
                        ORDER BY novel_content.create_time'''

                cursor.execute(sql, [work_id])
                result = cursor.fetchall()

                work_info = {
                    'work_list': [],
                    'author_info': [],
                    'word_count': 0
                }

                if result:
                    columns = [column[0] for column in cursor.description]
                    rows = [dict(zip(columns, row)) for row in result]

                    for row in rows:
                        create_time_dt = datetime.strptime(row['create_time'], '%Y-%m-%dT%H:%M:%S')
                        row['create_time'] = create_time_dt.strftime('%Y年%m月%d日 %H时%M分%S秒')
                        del row['content']

                    work_info['work_list'] = rows
                    belong_to_userid = rows[0]['belong_to_userid']

                    cursor.execute('SELECT * FROM users WHERE userid = %s', [belong_to_userid])
                    author_result = cursor.fetchone()

                    if author_result:
                        author_columns = [column[0] for column in cursor.description]
                        author_info = dict(zip(author_columns, author_result))
                        del author_info['password']
                        del author_info['token']
                        work_info['author_info'] = author_info

                        cursor.execute(
                            'SELECT SUM(CHAR_LENGTH(content)) FROM novel_content WHERE belong_to_series_id = %s',
                            [work_id])
                        work_info['word_count'] = cursor.fetchone()[0] or 0

                        watch_sql = 'SELECT COUNT(*) FROM user_watch_table WHERE type = %s AND workid = %s'
                        cursor.execute(watch_sql, ['novel', work_id])
                        work_info['watch_count'] = cursor.fetchone()[0]

                        like_sql = 'SELECT COUNT(*) FROM user_like_table WHERE type = %s AND workid = %s'
                        cursor.execute(like_sql, ['novel', work_id])
                        work_info['like_count'] = cursor.fetchone()[0]

                        is_like_sql = 'SELECT 1 FROM user_like_table WHERE type = %s AND workid = %s AND userid = %s'
                        cursor.execute(is_like_sql, ['novel', work_id, userid])
                        work_info['is_like'] = bool(cursor.fetchone())

                        collect_sql = 'SELECT COUNT(*) FROM user_collection_table WHERE type = %s AND workid = %s'
                        cursor.execute(collect_sql, ['novel', work_id])
                        work_info['collect_count'] = cursor.fetchone()[0]

                        is_collect_sql = 'SELECT 1 FROM user_collection_table WHERE type = %s AND workid = %s AND userid = %s'
                        cursor.execute(is_collect_sql, ['novel', work_id, userid])
                        work_info['is_collect'] = bool(cursor.fetchone())

                        return JsonResponse({'status': 'success', 'message': '数据获取成功', 'data': work_info},
                                            status=200)

                    else:
                        self.logger.warning(self.request_path(request) + '数据获取失败，失败原因：数据不存在')
                        return JsonResponse({'status': 'error', 'message': '数据不存在'}, status=400)
                else:
                    self.logger.warning(self.request_path(request) + '数据获取失败，失败原因：数据不存在')
                    return JsonResponse({'status': 'error', 'message': '数据不存在'}, status=400)

        except Exception as e:
            self.logger.error(self.request_path(request) + '数据获取失败，失败原因：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
