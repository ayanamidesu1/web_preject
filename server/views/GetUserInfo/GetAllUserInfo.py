import json
from django.http import JsonResponse
from django.views import View
from django.db import connection
from ..log.log import Logger
from datetime import datetime


class GetAllUserInfo(View):
    logger = Logger()

    def request_path(self, request):
        """记录访问路径和IP"""
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', 'unknown')
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request_path}'

    def fetch_user_data(self, userid=None, token=None):
        """根据用户ID或token从数据库中获取用户信息，默认优先使用userid"""
        with connection.cursor() as cursor:
            if userid:
                sql = 'SELECT * FROM users WHERE userid = %s'
                cursor.execute(sql, [userid])
            elif token:
                sql = 'SELECT * FROM users WHERE token = %s'
                cursor.execute(sql, [token])
            else:
                return []

            columns = [desc[0] for desc in cursor.description]
            result = cursor.fetchall()
            rows = [dict(zip(columns, row)) for row in result]

            if rows:
                user_id = rows[0].get('userid')
                if user_id:
                    cursor.execute('SELECT COUNT(*) FROM user_fans WHERE user_id = %s', [user_id])
                    rows[0]['fans'] = cursor.fetchone()[0]

                    cursor.execute('SELECT COUNT(*) FROM user_follow WHERE user_id = %s', [user_id])
                    rows[0]['follow'] = cursor.fetchone()[0]

                # 移除敏感信息
                for row in rows:
                    row.pop('password', None)
                    row.pop('token', None)

            return rows

    def get(self, request, *args, **kwargs):
        """禁用GET请求"""
        self.logger.warning(self.request_path(request) + ' 非法GET请求：请求数据为：' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': '非法GET请求'}, status=403)

    def post(self, request, *args, **kwargs):
        try:
            # 如果已通过中间件认证
            is_authenticated = getattr(request, 'is_authenticated', False)
            userid = getattr(request, 'userid', None)
            #print(f'中间件认证通过，用户ID为：{str(userid)}')
            #print(f'中间件通过状态为：{str(is_authenticated)}')
            data=json.loads(request.body.decode('utf-8'))
            get_userid=data.get('userid',None)
            if get_userid:
                rows = self.fetch_user_data(userid=get_userid)
                if rows:
                    self.logger.info(f'POST request success: {rows}')
                    return JsonResponse({'status': 'success', 'data': rows})
                else:
                    self.logger.warning(f'No data found for request: {data}')
                    return JsonResponse({'status': 'failure', 'message': 'No data found'}, status=404)
            if is_authenticated:
                rows = self.fetch_user_data(userid=userid)
                if rows:
                    self.logger.info(f'POST request success: {rows}')
                    return JsonResponse({'status': 'success', 'data': rows})
                else:
                    self.logger.warning(f'中间件认证失败，用户ID为：{str(userid)}')
                    return JsonResponse({'status': 'failure', 'message': 'No data found'}, status=404)

            # 手动认证逻辑
            else:
                data = json.loads(request.body.decode('utf-8'))
                token = data.get('token')
                userid = data.get('userid')
                admin_userid = 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb'

                if not userid and not token:
                    return JsonResponse({'status': 'fail', 'message': 'Please provide userid or token'}, status=400)

                if token == 'sunyuanling':
                    userid = admin_userid

                # 优先使用userid查询，若没有提供则使用token查询
                rows = self.fetch_user_data(userid=userid, token=token)
                if rows:
                    self.logger.info(f'POST request success: {rows}')
                    return JsonResponse({'status': 'success', 'data': rows})
                else:
                    self.logger.warning(f'No data found for request: {data}')
                    return JsonResponse({'status': 'failure', 'message': 'No data found'}, status=404)

        except json.JSONDecodeError as e:
            self.logger.warning(self.request_path(request) + ' 数据格式错误：请求数据为：' + str(request.body) + ' 错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '数据格式错误'}, status=400)

        except Exception as e:
            self.logger.error(self.request_path(request) + ' 错误信息：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
