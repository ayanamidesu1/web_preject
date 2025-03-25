from django.db import connection
from django.views import View
from django.http import JsonResponse
from datetime import datetime
from ..log.log import Logger
import json
from django.shortcuts import render


class SearchIllWork(View):
    logger = Logger()

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META['REMOTE_ADDR']
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return f'{request_ip}在{now}访问了{request_path}'

    def get(self, request):
        self.logger.warning(self.request_path(request) + '非法GET请求；请求内容为：' + str(request.GET))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            userid = getattr(request, 'userid', None)
            if not userid:
                self.logger.warning(f'{self.request_path(request)}；用户未登录')
                return JsonResponse({'status': 'error', 'message': '用户未登录'}, status=401)

            data = json.loads(request.body.decode('utf-8'))
            print(data)
            search_key = data.get('search_key', None)
            work_status = data.get('work_status', 'all')

            # 初步SQL和参数构建
            base_sql = "SELECT * FROM illustration_work WHERE 1=1"
            params = []

            # 处理关键字搜索（模糊匹配）
            if search_key and search_key!="":
                base_sql += " AND name LIKE %s"
                params.append(f"%{search_key}%")  # 模糊匹配，名称包含关键字

            # 处理状态筛选
            if work_status == 'fail':
                base_sql += " AND work_approved = %s"
                params.append(0)
            elif work_status == 'unaudited':
                base_sql += " AND work_approved = %s"
                params.append(2)
            elif work_status == 'pass':
                base_sql += " AND work_approved = %s"
                params.append(1)
            elif work_status == 'all':
                pass

            # 执行SQL查询
            with connection.cursor() as cursor:
                cursor.execute(base_sql, params)
                result = cursor.fetchall()

                if result:
                    columns = [column[0] for column in cursor.description]
                    rows = [dict(zip(columns, row)) for row in result]
                    return JsonResponse({'status': 'success', 'message': '搜索成功', 'data': rows}, status=200)

                return JsonResponse({'status': 'error', 'message': '未找到相关作品'}, status=404)

        except Exception as e:
            self.logger.error(f'{self.request_path(request)}；错误信息为：{e}')
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
