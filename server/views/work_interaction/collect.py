from django.db import connection
from django.http import JsonResponse
from django.views import View
from datetime import datetime
import json
from ..log.log import Logger


class Collect(View):
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
            token = data.get('token')
            userid=getattr(request,'userid',None)

            if not userid:
                with connection.cursor() as cursor:
                    cursor.execute('select userid from users where token=%s', [token])
                    result = cursor.fetchone()
                    userid = result[0] if result else None
                    if not result:
                        self.logger.error(
                            self.request_path(request) + '请求信息：' + str(request.POST) + '错误信息：无效的token')
                        return JsonResponse({'status': 'error', 'message': '无效的token'}, status=403)
            with connection.cursor() as cursor:
                operate_type = data.get('operate_type')
                work_id = int(data.get('work_id'))
                work_type = data.get('work_type')
                work_name = data.get('work_name')

                if operate_type == 'search':
                    sql = 'select * from user_collection_table where userid=%s and workid=%s and type=%s'
                    cursor.execute(sql, [userid, work_id, work_type])
                    if cursor.fetchone():
                        return JsonResponse({'status': 'success', 'data': 1, 'message': '已经收藏'}, status=200)
                    else:
                        return JsonResponse({'status': 'success', 'data': 0, 'message': '未收藏'}, status=200)
                if operate_type == 'count':
                    sql = 'select count(*) from user_collection_table where workid=%s and type=%s'
                    cursor.execute(sql, [work_id, work_type])
                    return JsonResponse({'status': 'success', 'data': cursor.fetchone()[0], 'message': '查询成功'},
                                        status=200)

                elif operate_type == 'add':
                    # 首先检查是否已经存在收藏记录
                    search_sql = 'select * from user_collection_table where userid=%s and workid=%s and type=%s'
                    cursor.execute(search_sql, [userid, work_id, work_type])
                    existing_like = cursor.fetchone()

                    if existing_like:
                        # 如果存在收藏记录，则删除记录并返回取消收藏的消息
                        delete_sql = 'delete from user_collection_table where userid=%s and workid=%s and type=%s'
                        cursor.execute(delete_sql, [userid, work_id, work_type])
                        if cursor.rowcount == 1:
                            self.logger.info(self.request_path(request) + '请求信息：' + str(request.POST) + '操作成功，取消收藏')
                            return JsonResponse({'status': 'success', 'message': '取消收藏成功', 'data': 0}, status=200)
                        else:
                            self.logger.error(self.request_path(request) + '请求信息：' + str(request.POST) + '操作失败')
                            return JsonResponse({'status': 'error', 'message': '取消收藏失败', 'data': 0}, status=500)
                    else:
                        # 如果不存在收藏记录，则插入新的收藏记录
                        insert_sql = ('insert into user_collection_table(userid, workid, workname, time, type,is_open,is_collection) values (%s,'
                                      '%s,%s,%s,%s,%s,%s)')
                        cursor.execute(insert_sql, [userid, work_id, work_name, now, work_type,1,1])
                        if cursor.rowcount == 1:
                            self.logger.info(self.request_path(request) + '请求信息：' + str(request.POST) + '操作成功，新增收藏')
                            return JsonResponse({'status': 'success', 'message': '收藏成功', 'data': 1}, status=200)
                        else:
                            self.logger.error(self.request_path(request) + '请求信息：' + str(request.POST) + '操作失败')
                            return JsonResponse({'status': 'error', 'message': '收藏失败', 'data': 0}, status=500)

                else:
                    self.logger.error(
                        self.request_path(request) + '请求信息：' + str(request.POST) + '错误信息：无效的操作类型')
                    return JsonResponse({'status': 'error', 'message': '无效的操作类型'}, status=400)

        except json.JSONDecodeError as e:
            self.logger.error(
                self.request_path(request) + '发生异常，异常信息为：' + str(e) + '请求信息：' + str(request.POST))
            return JsonResponse({'status': 'error', 'message': '请求数据格式错误'}, status=400)
        except Exception as e:
            self.logger.error(
                self.request_path(request) + '发生异常，异常信息为：' + str(e) + '请求信息：' + str(request.POST))
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)
