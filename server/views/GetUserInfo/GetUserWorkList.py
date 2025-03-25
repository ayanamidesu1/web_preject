from django.db import connection
from django.views import View
from django.http import JsonResponse
import json
from ..log.log import Logger
from datetime import datetime


class GetUserWorkList(View):
    logger = Logger()

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', '未知 IP')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f'请求IP：{request_ip}，请求地址： {request_path}，时间： {now}；'

    def get(self, request):
        self.logger.warning(str(self.request_path(request)) + '请求方式：GET，非法访问' + '请求信息：' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = getattr(request, 'userid', None)
            offset = data.get('offset', 0)
            limit = data.get('limit', 10000)
            get_userid=data.get('userid',None)
            if get_userid:
                userid=get_userid

            if not userid:
                raise ValueError("用户ID缺失")

            # SQL查询字典
            sql_query_dict = {
                'ill': 'SELECT *, "ill" AS type FROM illustration_work '
                       'WHERE belong_to_user_id=%s and work_approved=1 '
                       'ORDER BY create_time DESC LIMIT %s OFFSET %s',
                'comic': 'SELECT *, "comic" AS type FROM comic WHERE belong_to_userid=%s and work_approved=1'
                         ' ORDER BY create_time DESC LIMIT %s OFFSET %s',
                'novel': 'SELECT *, "novel" AS type FROM novel_work'
                         ' WHERE belong_to_userid=%s and work_approved=1 '
                         'ORDER BY work_create_time DESC LIMIT %s OFFSET %s'
            }

            # 获取总作品数量的SQL查询
            sql_get_all_work_count = {
                'ill': 'SELECT COUNT(*) as work_count FROM illustration_work WHERE belong_to_user_id=%s',
                'comic': 'SELECT COUNT(*) as work_count FROM comic WHERE belong_to_userid=%s',
                'novel': 'SELECT COUNT(*) as work_count FROM novel_work WHERE belong_to_userid=%s'
            }

            work_list = {}
            total_count = {}

            with connection.cursor() as cursor:
                # 获取作品列表
                for work_type, query in sql_query_dict.items():
                    cursor.execute(query, [userid, limit, offset])
                    columns = [desc[0] for desc in cursor.description]
                    result = cursor.fetchall()
                    rows = [dict(zip(columns, row)) for row in result]
                    work_list[work_type] = rows

                # 获取总作品数
                for work_type, query in sql_get_all_work_count.items():
                    cursor.execute(query, [userid])
                    total_count[work_type] = cursor.fetchone()[0]  # 直接获取数量

            # 记录日志
            self.logger.info(
                str(self.request_path(request)) + '请求方式：POST，请求信息：' + str(request.body) + '请求成功')

            # 返回数据
            return JsonResponse({
                'status': 'success',
                'data': work_list,
                'total_count': total_count  # 返回每种类型的总作品数
            })

        except json.JSONDecodeError as e:
            self.logger.error(str(self.request_path(request)) + '请求方式：POST，请求信息：' + str(
                request.body) + ' JSON 解码错误: ' + str(e))
            return JsonResponse({'status': 'error', 'message': '请求数据格式错误'}, status=400)

        except ValueError as e:
            self.logger.error(
                str(self.request_path(request)) + '请求方式：POST，请求信息：' + str(request.body) + ' 参数错误: ' + str(
                    e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

        except Exception as e:
            self.logger.error(
                str(self.request_path(request)) + '请求方式：POST，请求信息：' + str(request.body) + ' 服务器错误: ' + str(
                    e))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
