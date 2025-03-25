from django.db import connection
from django.views import View
from django.http import JsonResponse
import json
from datetime import datetime
from ..log.log import Logger


class GetFriendList(View):
    logger = Logger()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': 'error', 'message': '请求方式错误，请使用 POST 请求'}, status=405)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = data.get('userid')
            if not userid:
                return JsonResponse({'status': 'error', 'message': '缺少 userid 参数'}, status=400)

            with connection.cursor() as cursor:
                sql = 'SELECT * FROM friends_table WHERE userid=%s'
                cursor.execute(sql, [userid])
                columns = [desc[0] for desc in cursor.description]
                result = cursor.fetchall()

                if result:
                    rows = [dict(zip(columns, row)) for row in result]
                    self.logger.info('用户 ID 为 {} 的用户的好友列表为 {}'.format(userid, rows))
                    return JsonResponse({'status': 'success', 'data': rows})
                else:
                    self.logger.info('用户 ID 为 {} 的用户的好友列表为空，请求数据 {}'.format(userid, data))
                    return JsonResponse({'status': 'success', 'data': []}, status=204)

        except json.JSONDecodeError:
            self.logger.error('JSON 解析错误')
            return JsonResponse({'status': 'error', 'message': 'JSON 解析错误'}, status=400)
        except Exception as e:
            self.logger.error(f'服务器错误: {e}')
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
