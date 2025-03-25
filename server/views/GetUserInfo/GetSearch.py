from json import JSONDecodeError
from django.db import connection
from django.views import View
from django.http import JsonResponse
import json
from datetime import datetime
from ..log.log import Logger

class GetSearch(View):
    logger = Logger()
    # 请求地址
    path = '/api/getSearch'
    # 请求IP地址
    path_ip = '127.0.0.1'

    def get(self, request, *args, **kwargs):
        self.logger.warning(
            self.request_path(request) + str('请求方式：GET,请求参数：' + str(request.GET) + str('非法访问')))
        return JsonResponse({'status': 'success', 'message': '请求方式错误'}, status=405)

    def post(self, request, *args, **kwargs):
        self.logger.info(self.request_path(request) + str('请求方式：POST,请求参数：' + str(request.POST)))
        try:
            data = json.loads(request.body.decode('utf-8'))
            search_key = data.get('search_key', '').strip()

            if not search_key:
                raise ValueError("搜索关键词不能为空")

            combined_results = []
            search_pattern = f"%{search_key}%"

            with connection.cursor() as cursor:
                # 查询插画信息
                sql = """
                SELECT *, 'ill' AS type FROM illustration_work 
                WHERE name LIKE %s OR belong_to_user LIKE %s OR work_tags LIKE %s
                """
                cursor.execute(sql, (search_pattern, search_pattern, search_pattern))
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]
                combined_results.extend(rows)

                # 查询漫画信息
                sql = """
                SELECT *, 'comic' AS type FROM comic
                WHERE work_name LIKE %s OR belong_to_user LIKE %s OR work_tags LIKE %s
                """
                cursor.execute(sql, (search_pattern, search_pattern, search_pattern))
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]
                combined_results.extend(rows)

                # 查询小说信息
                sql = """
                SELECT *, 'novel' AS type FROM novel_work
                WHERE work_name LIKE %s OR belong_to_username LIKE %s OR work_tags LIKE %s
                """
                cursor.execute(sql, (search_pattern, search_pattern, search_pattern))
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]
                combined_results.extend(rows)

                # 查询用户信息
                sql="""
                select userid,username,user_avatar,user_self_introduction ,'user' as type from users where username like %s 
                """
                cursor.execute(sql,(search_pattern,))
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                rows = [dict(zip(columns, row)) for row in result]
                combined_results.extend(rows)

            return JsonResponse({'status': 'success', 'message': '请求成功', 'data': combined_results}, status=200)
        except JSONDecodeError as e:
            self.logger.error(self.request_path(request) +
                              str('请求方式：POST,请求参数：' + str(request.POST) + str('异常信息：' + str(e))))
            return JsonResponse({'status': 'error', 'message': '请求参数错误'}, status=400)
        except ValueError as e:
            self.logger.error(self.request_path(request) +
                              str('请求方式：POST,请求参数：' + str(request.POST) + str('异常信息：' + str(e))))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            self.logger.error(self.request_path(request) +
                              str('请求方式：POST,请求参数：' + str(request.POST) + str('异常信息：' + str(e))))
            return JsonResponse({'status': 'error', 'message': '服务器内部错误'}, status=500)

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        info = '请求地址：' + request_path + ' 请求IP地址：' + request_ip + ' 请求时间：' + now
        return info
