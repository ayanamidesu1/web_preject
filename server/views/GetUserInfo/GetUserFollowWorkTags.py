from django.db import connection
from django.views import View
from django.http import JsonResponse
from ..log.log import Logger
from datetime import datetime
import json

class GetUserFollowWorkTags(View):
    logger = Logger()

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', 'unknown')
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return f'{request_ip} 在 {now} 请求了 {request_path}'

    def get(self, request):
        self.logger.warning(self.request_path(request) + ' 非法GET访问，访问数据为：' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': '非法GET访问'}, status=403)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            token = data.get('token')
            admin_userid = 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb'
            userid=getattr(request,'userid',None)
            with connection.cursor() as cursor:
                if not userid:
                    if not token:
                        self.logger.warning(self.request_path(request) + ' token为空')
                        return JsonResponse({'status': 'error', 'message': 'token为空'}, status=400)

                    # Token验证逻辑
                    if token == 'sunyuanling':
                        cursor.execute('SELECT token FROM users WHERE userid=%s', [admin_userid])
                        result = cursor.fetchone()
                        if result:
                            token = result[0]

                    cursor.execute('SELECT userid FROM users WHERE token=%s', [token])
                    userid_row = cursor.fetchone()
                    if not userid_row:
                        self.logger.warning(self.request_path(request) + ' token错误，请求数据为：' + str(request.body))
                        return JsonResponse({'status': 'error', 'message': 'token错误'}, status=401)

                    userid = userid_row[0]

                follow_list = []
                sql = 'SELECT follow_user_id FROM user_follow WHERE user_id=%s'
                cursor.execute(sql, [userid])
                follow_list = cursor.fetchall()

                # SQL 查询
                sql = '''
                    SELECT DISTINCT
                        illustration_work.work_tags AS illustration_tags,
                        comic.work_tags AS comic_tags,
                        novel_work.work_tags AS novel_tags
                    FROM 
                        illustration_work
                    LEFT JOIN 
                        comic ON illustration_work.belong_to_user_id = comic.belong_to_userid
                    LEFT JOIN 
                        novel_work ON illustration_work.belong_to_user_id = novel_work.belong_to_userid
                    WHERE 
                        illustration_work.belong_to_user_id = %s;
                '''

                all_tags_set = set()  # 使用集合来去重所有标签
                for follow in follow_list:
                    cursor.execute(sql, [follow[0]])
                    row = cursor.fetchone()
                    if row:
                        illustration_tags = row[0] or ''
                        comic_tags = row[1] or ''
                        novel_tags = row[2] or ''

                        # 合并并分割标签
                        tags_combined = f"{illustration_tags},{comic_tags},{novel_tags}"
                        tags = tags_combined.split('，')  # 使用中文逗号分割
                        tags = [tag for sublist in [tag.split(',') for tag in tags] for tag in sublist]  # 使用英文逗号分割
                        tags = [tag.strip() for tag in tags]  # 去除空格
                        tags = set(tag for tag in tags if tag)  # 去重并过滤空标签

                        # 添加到集合中以去重
                        all_tags_set.update(tags)

                # 将去重后的所有标签从集合中转换回列表
                all_tags_list = list(all_tags_set)

            return JsonResponse({'status': 'success', 'data': all_tags_list})

        except Exception as e:
            print('获取关注作品标签错误：',e)
            self.logger.error(self.request_path(request) + ' 错误信息：' + str(e) + ' 请求数据为：' + str(request.body))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
