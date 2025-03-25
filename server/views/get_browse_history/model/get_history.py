from django.db import connection
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from datetime import datetime
import json
from ..log.log import Logger

class GetHistory(View):
    logger = Logger()

    def _request_info(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return f'{request_ip} 在 {now} 请求了 {request.path}, 请求内容为: {request.body.decode("utf-8")}'

    def _get_work_details(self, cursor, work_id, work_type):
        work_queries = {
            'ill': 'SELECT * FROM illustration_work WHERE Illustration_id = %s',
            'comic': 'SELECT * FROM comic WHERE id = %s',
            'novel': 'SELECT * FROM novel_work WHERE work_id = %s'
        }
        query = work_queries.get(work_type)
        if query:
            cursor.execute(query, [work_id])
            result = cursor.fetchone()
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, result)) if result else None
        return None

    def _fetch_user_history(self, userid, limit, offset):
        query = '''
        SELECT * FROM user_watch_table WHERE userid = %s LIMIT %s OFFSET %s
        '''
        with connection.cursor() as cursor:
            cursor.execute(query, [userid, limit, offset])
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in result]

    def _enrich_history(self, history_rows):
        with connection.cursor() as cursor:
            for row in history_rows:
                work_type = row.get('type')
                if work_type:
                    row['work'] = self._get_work_details(cursor, row.get('workid',''), work_type)
        return history_rows

    def get(self, request):
        self.logger.warning(f'非法GET请求；{self._request_info(request)}')
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = str(getattr(request, 'userid', None))
            is_authenticated = getattr(request, 'is_authenticated', None)

            if not is_authenticated:
                self.logger.warning(f'未登录用户尝试访问：{self._request_info(request)}')
                return JsonResponse({'status': 'fail', 'message': '未登录'}, status=401)

            if not userid:
                self.logger.warning(f'非法用户尝试访问：{self._request_info(request)}')
                return JsonResponse({'status': 'fail', 'message': '非法用户'}, status=401)

            limit = data.get('limit', 1000)
            offset = data.get('offset', 0)
            history = self._fetch_user_history(userid, limit, offset)
            enriched_history = self._enrich_history(history)

            return JsonResponse({'status': 'success', 'message': '获取成功', 'data': enriched_history})

        except Exception as e:
            print(e)
            self.logger.error(f'服务器内部错误；{self._request_info(request)},错误信息：{str(e)}')
            return JsonResponse({'status': 'fail', 'message': '服务器内部错误'}, status=500)
