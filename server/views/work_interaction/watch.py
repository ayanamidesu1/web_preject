from django.db import connection
from django.http import JsonResponse
from django.views import View
from datetime import datetime
import json
from ..log.log import Logger


class Watch(View):
    logger = Logger()

    def request_path(self, request):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        return f'{request_ip}访问了{request_path}接口，时间为{now}'

    def get(self, request):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.logger.warning(self.request_path(request) + '请求数据为：' + str(request.GET))
        return JsonResponse({'status': 'error', 'message': '非法GET请求'}, status=403)

    def post(self, request, *args, **kwargs):
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            userid=getattr(request,'userid',None)
            token = data.get('token')
            if not userid:
                with connection.cursor() as cursor:
                    if token:
                        cursor.execute('select userid from users where token=%s', [token])
                        userid = cursor.fetchone()
                        if not userid:
                            self.logger.info(
                                self.request_path(request) + '请求数据为：' + str(request.POST) + '错误信息为：token无效')
                            return JsonResponse({'status': 'error', 'message': 'token无效'}, status=403)
            with connection.cursor() as cursor:
                work_id = int(data.get('work_id'))
                work_type = data.get('work_type')
                work_name = data.get('work_name')
                sql='select count(*) from user_watch_table where type=%s and workid=%s'
                cursor.execute(sql, [work_type, work_id])
                count=cursor.fetchone()[0]

                search_sql = 'select * from user_watch_table where userid=%s and workid=%s and type=%s'
                cursor.execute(search_sql, [userid, work_id, work_type])

                if cursor.fetchone():  # 如果存在则更新
                    sql = 'update user_watch_table set time=%s where userid=%s and workid=%s and type=%s'
                    cursor.execute(sql, [now, userid, work_id, work_type])
                    if cursor.rowcount >= 1:
                        self.logger.info(self.request_path(request) + '请求数据为：' + str(request.POST) + '操作成功')
                        return JsonResponse({'status': 'success', 'message': '更新观看数据','count':count}, status=200)
                else:
                    sql = 'insert into user_watch_table (userid,workid,workname,time,type)values(%s,%s,%s,%s,%s)'
                    cursor.execute(sql, [userid, work_id, work_name, now, work_type])
                    if cursor.rowcount >= 1:
                        self.logger.info(self.request_path(request) + '请求数据为：' + str(request.POST) + '操作成功')
                        return JsonResponse({'status': 'success', 'message': '新增一个观看','count':count}, status=200)

                self.logger.warning(self.request_path(request) + '请求数据为：' + str(request.POST) + '操作失败')
                return JsonResponse({'status': 'error', 'message': '新增失败'}, status=500)
        except json.JSONDecodeError as e:
            print(e)
            self.logger.error(self.request_path(request) + '请求数据为：' + str(request.POST) + '错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '请求数据格式错误'}, status=400)
        except Exception as e:
            print(e)
            self.logger.error(self.request_path(request) + '请求数据为：' + str(request.POST) + '错误信息为：' + str(e))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
