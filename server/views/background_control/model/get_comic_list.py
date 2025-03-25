from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import json
from datetime import datetime
from .log.log import Logger

logger = Logger()

class GetComicList(View):
    def _request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return f'{request_ip}在{now}请求了{request_path}'

    def get(self, request):
        logger.warning(f'{self._request_path(request)} - 非法GET请求，请求内容为：{request.GET}')
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = str(getattr(request, 'userid', None))
            is_authenticated = getattr(request, 'is_authenticated', None)

            if not is_authenticated:
                logger.warning(f'{self._request_path(request)} - 用户未登录，非法访问')
                return JsonResponse({'status': 'error', 'message': '未登录'}, status=401)

            limit = data.get('limit', 10)
            offset = data.get('offset', 0)

            with connection.cursor() as cursor:
                # 获取用户权限
                cursor.execute('SELECT account_permissions FROM users WHERE userid = %s', [userid])
                account_permissions = cursor.fetchone()

                if not account_permissions or account_permissions[0] not in ['1', '2', 1, 2]:
                    logger.warning(f'{self._request_path(request)} - 非授权人员访问')
                    return JsonResponse({'status': 'error', 'message': '权限不足'}, status=403)

                # 查询漫画列表
                sql = ('SELECT comic.*, users.userid, users.user_avatar, users.username '
                       'FROM comic '
                       'LEFT JOIN users ON users.userid = comic.belong_to_userid '
                       'ORDER BY comic.create_time DESC '
                       'LIMIT %s OFFSET %s')

                cursor.execute(sql, [limit, offset])
                result = cursor.fetchall()

                if result:
                    columns = [col[0] for col in cursor.description]
                    rows = [dict(zip(columns, row)) for row in result]
                    # 查询总数
                    cursor.execute('SELECT COUNT(*) FROM comic')
                    total = cursor.fetchone()[0]
                    return JsonResponse({
                        'status': 'success',
                        'data': {
                            'work_list': rows,
                            'total': total
                        }
                    }, status=200)
                else:
                    return JsonResponse({'status': 'success', 'data': []}, status=200)

        except json.JSONDecodeError:
            logger.error(f'{self._request_path(request)} - 请求数据格式错误')
            return JsonResponse({'status': 'error', 'message': '无效的JSON数据'}, status=400)

        except Exception as e:
            logger.error(f'{self._request_path(request)} - 服务器错误: {str(e)}')
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
