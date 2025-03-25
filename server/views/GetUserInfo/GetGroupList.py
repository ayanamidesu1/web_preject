from django.db import connection
from django.views import View
from django.http import JsonResponse
from ..log.log import Logger
import json
from datetime import datetime


class GetGroupList(View):
    logger = Logger()

    def get(self, request, *args, **kwargs):
        now = datetime.now()
        self.logger.warning(f'时间：{now}，非法访问：{request.META["REMOTE_ADDR"]}，尝试获取群组列表')
        return JsonResponse({'status': 'error', 'message': '非法的方法'}, status=405)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = data.get('userid')
            if not userid:
                self.logger.error('请求中缺少userid')
                return JsonResponse({'status': 'error', 'message': '缺少userid'}, status=400)

            with connection.cursor() as cursor:
                sql = '''
                    SELECT * FROM `group`
                    WHERE userid = %s 
                '''
                cursor.execute(sql, [userid, ])
                columns = [desc[0] for desc in cursor.description]
                result = cursor.fetchall()
                if result:
                    rows = [dict(zip(columns, row)) for row in result]
                    self.logger.info(f'请求者ID：{userid}，获取群组列表成功')
                    return JsonResponse({'status': 'success', 'data': rows}, status=200)
                else:
                    self.logger.info(f'请求者ID：{userid}，获取群组列表成功，但未加入任何群组')
                    return JsonResponse({'status': 'success', 'data': [], 'message': '没有加入任何群组'}, status=200)
        except json.JSONDecodeError:
            self.logger.error('JSON 解析错误')
            return JsonResponse({'status': 'error', 'message': 'JSON 解析错误'}, status=400)
        except Exception as e:
            self.logger.error(f'服务器异常: {e}')
            print(e)
            return JsonResponse({'status': 'fail', 'message': '服务器异常'}, status=500)


class GetGroupInfo(View):
    logger = Logger()

    def path(self, request):
        request_path = request.path
        request_ip = request.META['REMOTE_ADDR']
        now = datetime.now()
        return f'时间：{now}，访问地址信息：{request_ip}，尝试获取群组信息，请求地址：{request_path}'

    def get(self, request, *args, **kwargs):
        self.logger.warning(self.path(request))
        return JsonResponse({'status': 'error', 'message': '非法的方法'}, status=405)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = data.get('userid')
            group_id = data.get('group_id')

            if not userid or not group_id:
                self.logger.warning(f'请求信息：{data}; 请求地址信息：{self.path(request)}，尝试获取群组信息')
                return JsonResponse({'status': 'warning', 'message': '缺少重要参数'}, status=400)

            with connection.cursor() as cursor:
                sql = 'SELECT * FROM `group` WHERE group_id = %s AND userid = %s'
                cursor.execute(sql, [group_id, userid])
                columns = [desc[0] for desc in cursor.description]
                result = cursor.fetchall()

                if result:
                    rows = [dict(zip(columns, row)) for row in result]
                    self.logger.info(
                        f'请求信息：{data}; 请求地址：{self.path(request)}; 请求者ID：{userid}，获取群组信息成功')
                    return JsonResponse({'status': 'success', 'data': rows}, status=200)
                else:
                    self.logger.info(
                        f'请求信息：{data}; 请求地址：{self.path(request)}; 请求者ID：{userid}，获取群组信息成功，但未加入任何群组')
                    return JsonResponse({'status': 'success', 'data': [], 'message': '没有加入任何群组'}, status=200)

        except json.JSONDecodeError:
            self.logger.error(f'请求信息：{request.body}; 请求地址信息：{self.path(request)}; 错误信息：JSON 解析错误')
            return JsonResponse({'status': 'error', 'message': 'JSON 解析错误'}, status=400)
        except Exception as e:
            self.logger.error(f'请求信息：{request.body}; 请求地址信息：{self.path(request)}; 服务器异常: {e}')
            return JsonResponse({'status': 'fail', 'message': '服务器异常'}, status=500)


class GroupControlInfo(View):
    logger = Logger()

    def get(self, request, *args, **kwargs):
        now = datetime.now()
        self.logger.warning(f'时间：{now}，非法访问：{request.META["REMOTE_ADDR"]}，尝试获取群组信息')
        return JsonResponse({'status': 'error', 'message': '非法的方法'}, status=405)

    def post(self, request, *args, **kwargs):
        now = datetime.now()
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = data.get('userid')
            group_id = data.get('group_id')

            if not userid or not group_id:
                self.logger.error(
                    f'时间：{now}，请求中缺少userid或group_id，请求者ID：{userid}，请求地址：{request.path}，尝试获取群组信息')
                return JsonResponse({'status': 'error', 'message': '缺少重要参数'}, status=400)

            with connection.cursor() as cursor:
                sql = '''
                    SELECT role FROM `group`
                    WHERE `group`.group_id = %s AND (create_user_id = %s OR admin_id = %s or member_id = %s or userid=%s)
                '''
                cursor.execute(sql, [group_id, userid, userid, userid, userid])
                result = cursor.fetchone()

                if result:
                    self.logger.info(
                        f'时间：{now}，请求者ID：{userid}，请求地址：{request.path}，尝试获取群组信息成功')
                    return JsonResponse({'status': 'success', 'data': result}, status=200)
                else:
                    self.logger.info(
                        f'时间：{now}，请求者ID：{userid}，请求地址：{request.path}，尝试获取群组信息失败，没有加入群聊')
                    return JsonResponse({'status': 'error', 'message': '没有加入群聊'}, status=403)

        except json.JSONDecodeError:
            self.logger.error(f'时间：{now}，请求地址：{request.path}，JSON 解析错误')
            return JsonResponse({'status': 'error', 'message': 'JSON 解析错误'}, status=400)
        except Exception as e:
            self.logger.error(f'时间：{now}，请求地址：{request.path}，服务器异常: {e}')
            print(e)
            return JsonResponse({'status': 'fail', 'message': '服务器异常'}, status=500)
