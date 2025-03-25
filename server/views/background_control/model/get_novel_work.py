from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import json
from datetime import datetime
from .log.log import Logger

class GetNovelWork(View):
    logger = Logger()

    def _request_path(self,request):
        request_path=request.path
        request_ip=request.META.get('REMOTE_ADDR')
        now=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        content=request.body.decode('utf-8')
        return f'{request_ip}在{now}请求了{request_path},请求内容为：{content}'
    def get(self,request):
        self.logger.warning('非法get请求；请求内容为：'+self._request_path(request))
        return render(request,'404.html',status=404)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = str(getattr(request, 'userid', None))
            is_authenticated = getattr(request, 'is_authenticated', None)
            if is_authenticated:
                sql = '''SELECT account_permissions FROM users WHERE userid=%s'''
                with connection.cursor() as cursor:
                    cursor.execute(sql, [userid])
                    account_permissions = cursor.fetchone()[0]
                    if account_permissions in ['1', '2', 1, 2]:
                        limit = data.get('limit', 10)
                        offset = data.get('offset', 0)
                        sql = '''SELECT novel_work.*, 
                                        users.userid, 
                                        users.user_avatar, 
                                        users.username,
                                        SUM(CHAR_LENGTH(novel_content.content)) as "novel_word_count"
                                 FROM novel_work 
                                 LEFT JOIN users ON users.userid = novel_work.belong_to_userid 
                                 LEFT JOIN novel_content ON novel_content.belong_to_series_id = novel_work.work_id
                                 GROUP BY novel_work.work_id
                                 LIMIT %s OFFSET %s'''
                        cursor.execute(sql, [limit, offset])
                        result = cursor.fetchall()
                        columns = [column[0] for column in cursor.description]
                        rows = [dict(zip(columns, row)) for row in result]
                        if result:
                            count_sql = '''SELECT COUNT(*) FROM novel_work'''
                            cursor.execute(count_sql)
                            count = cursor.fetchone()[0]
                            return JsonResponse({
                                'status': 'success',
                                'data': {
                                    'work_list': rows,
                                    'total': count
                                }
                            }, status=200)
                        else:
                            return JsonResponse({'status': 'fail', 'message': '没有作品'}, status=404)
                    else:
                        return JsonResponse({'status': 'fail', 'message': '权限不足'}, status=403)
            else:
                return JsonResponse({'status': 'fail', 'message': '用户未登录'}, status=401)

        except Exception as e:
            self.logger.error('获取小说作品列表失败；请求内容为：' + self._request_path(request) + str(e))
            print('\n', e)
            return JsonResponse({'status': 'fail', 'message': '服务器错误'}, status=500)
