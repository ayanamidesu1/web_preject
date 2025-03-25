import uuid

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..log.log import Logger
from datetime import datetime, timedelta
import json
from django.contrib.auth import authenticate, login
import time


class NoticeOperations(View):
    logger = Logger()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql_dict = {
        'add': 'INSERT INTO notice (title, content, author_id, author_name, create_time, publish_time, '
               'expire_time, status, category, attachment_url, is_important, last_modified_time) '
               'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        'delete': 'DELETE FROM notice WHERE id = %s',
        'update': 'UPDATE notice SET title = %s, content = %s, author_id = %s, author_name = %s, create_time = %s, '
                  'publish_time = %s, expire_time = %s, category = %s, attachment_url = %s, last_modified_time = %s '
                  ',status=%s,priority=%s,category=%s,is_important=%s WHERE id = %s',
        'search': 'SELECT * FROM notice order by last_modified_time desc LIMIT %s OFFSET %s ',
        'count': 'SELECT COUNT(*) FROM notice'
    }

    def get_request_info(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f'{request_ip}在{now}访问了{request_path}页面'

    def get(self, request):
        self.logger.warning(f'{self.get_request_info(request)} - 非法访问：访问内容为GET {str(request.GET)}')
        return JsonResponse({'status': 'failed', 'message': '非法访问'}, status=403)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            print('公告：',data)
            operate_type = data.get('operate_type')
            userid = getattr(request,'userid',None)
            username=''
            if userid:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT username FROM users WHERE userid = %s', [userid])
                    username = cursor.fetchone()[0]
                    if not username:
                        self.logger.warning(f'{self.get_request_info(request)} - 访问失败：用户不存在 {str(request.body)}')
                        return JsonResponse({'status': 'failed', 'message': '用户不存在'}, status=404)


            if not userid:
                self.logger.warning(f'{self.get_request_info(request)} - 访问失败：缺少参数userid {str(request.body)}')
                return JsonResponse({'status': 'failed', 'message': '缺少参数userid'}, status=400)

            if not operate_type:
                self.logger.warning(
                    f'{self.get_request_info(request)} - 访问失败：缺少参数operate_type {str(request.body)}')
                return JsonResponse({'status': 'failed', 'message': '缺少参数operate_type'}, status=400)

            if operate_type == 'add':

                if userid != 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb':
                    self.logger.warning(f'{self.get_request_info(request)} - 访问失败：权限不足 {str(request.body)}')
                    return JsonResponse({'status': 'failed', 'message': '权限不足'}, status=403)

                with connection.cursor() as cursor:
                    cursor.execute(self.sql_dict['add'], [
                        data['title'], data['content'], userid, username, self.now,
                        data['publish_time'], data['expire_time'], data['status'], data['category'],
                        data.get('attachment_url'), data.get('is_important'),
                        self.now
                    ])
                self.logger.info(f'{self.get_request_info(request)} - 公告添加成功：{str(data)}')
                return JsonResponse({'status': 'success', 'message': '公告添加成功'}, status=201)

            elif operate_type == 'delete':
                if userid != 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb':
                    self.logger.warning(f'{self.get_request_info(request)} - 访问失败：权限不足 {str(request.body)}')
                    return JsonResponse({'status': 'failed', 'message': '权限不足'}, status=403)
                notice_id = data.get('id')
                if not notice_id:
                    self.logger.warning(f'{self.get_request_info(request)} - 访问失败：缺少参数id {str(request.body)}')
                    return JsonResponse({'status': 'failed', 'message': '缺少参数id'}, status=400)

                with connection.cursor() as cursor:
                    cursor.execute(self.sql_dict['delete'], [notice_id])
                    if cursor.rowcount == 0:
                        self.logger.warning(
                            f'{self.get_request_info(request)} - 访问失败：公告不存在 {str(request.body)}')
                        return JsonResponse({'status': 'failed', 'message': '公告不存在'}, status=404)
                self.logger.info(f'{self.get_request_info(request)} - 公告删除成功：{str(data)}')
                return JsonResponse({'status': 'success', 'message': '公告删除成功'}, status=200)

            elif operate_type == 'update':
                if userid != 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb':
                    self.logger.warning(f'{self.get_request_info(request)} - 访问失败：权限不足 {str(request.body)}')
                    return JsonResponse({'status': 'failed', 'message': '权限不足'}, status=403)
                id = data.get('id')

                with connection.cursor() as cursor:
                    cursor.execute(self.sql_dict['update'], [
                        data['title'], data['content'], userid, username, self.now,
                        data['publish_time'], data['expire_time'], data['category'], data.get('attachment_url'),
                        self.now, data.get('status'),data.get('priority'),data.get('category'),data.get('is_important'), id
                    ])
                self.logger.info(f'{self.get_request_info(request)} - 公告更新成功：{str(data)}')
                return JsonResponse({'status': 'success', 'message': '公告更新成功'}, status=200)

            elif operate_type == 'search':
                page = data.get('page', 1)
                per_page = data.get('per_page', 10)
                offset = (page - 1) * per_page

                with connection.cursor() as cursor:
                    cursor.execute(self.sql_dict['search'], [per_page, offset])
                    columns = [desc[0] for desc in cursor.description]
                    result = cursor.fetchall()
                    rows = [dict(zip(columns, row)) for row in result]

                    cursor.execute(self.sql_dict['count'])
                    total_count = cursor.fetchone()[0]

                return JsonResponse(
                    {'status': 'success', 'data': rows, 'total_count': total_count, 'page': page, 'per_page': per_page},
                    status=200)
            elif operate_type == 'key_search':
                key = data.get('key')
                sql = 'select * from notice where title like %s or id like %s or author_name like %s'
                with connection.cursor() as cursor:
                    cursor.execute(sql, [key, key, key])
                    columns = [desc[0] for desc in cursor.description]
                    result = cursor.fetchall()
                    rows = [dict(zip(columns, row)) for row in result]
                    return JsonResponse({'status': 'success', 'data': rows}, status=200)

            else:
                self.logger.warning(
                    f'{self.get_request_info(request)} - 访问失败：无效的操作类型{operate_type} {str(request.body)}')

                return JsonResponse({'status': 'failed', 'message': '无效的操作类型'}, status=400)

        except json.JSONDecodeError as e:
            print(e)
            self.logger.error(f'{self.get_request_info(request)} - 访问失败：JSONDecodeError {str(e)}')
            return JsonResponse({'status': 'failed', 'message': '请求数据格式错误'}, status=400)
        except Exception as e:
            self.logger.error(f'{self.get_request_info(request)} - 访问失败：Exception {str(e)}')
            print(e)
            return JsonResponse({'status': 'failed', 'message': '服务器内部错误'}, status=500)


class ControlNoticeLogin(View):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger = Logger()

    def create_uuid(self):
        return str(uuid.uuid4())

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        return f'访问IP：{request_ip}，访问路径：{request_path}，时间：{self.now}'

    def get(self, request):
        self.logger.warning(f'{self.request_path(request)} - 访问失败：无效的请求方法')
        return JsonResponse({'status': 'failed', 'message': '无效的请求方法'}, status=400)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = data.get('userid')
            password = data.get('password')
            token = data.get('token')
            token_sql = 'SELECT * FROM users WHERE userid=%s OR token=%s'

            with connection.cursor() as cursor:
                cursor.execute(token_sql, [userid, token])
                token_result = cursor.fetchone()

                if token_result:
                    columns = [desc[0] for desc in cursor.description]
                    row = dict(zip(columns, token_result))

                    # Token存在，检查其有效性
                    if token:
                        token_createtime = row.get('token_createtime')
                        token_value = row.get('token')
                        userid = row.get('userid')

                        if token_createtime:
                            token_createtime = datetime.strptime(token_createtime, '%Y-%m-%d %H:%M:%S')
                            token_expiration = token_createtime + timedelta(hours=24)

                            # Token未过期且正确
                            if datetime.now() < token_expiration and token_value == token:
                                new_token = self.create_uuid()
                                new_token_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                update_token_sql = 'UPDATE users SET token=%s, token_createtime=%s WHERE userid=%s'
                                cursor.execute(update_token_sql, [new_token, new_token_time, userid])
                                cursor.connection.commit()
                                print(f'{token}\t{new_token}\ttoken登录，token已更新')
                                return JsonResponse(
                                    {'status': 'success', 'message': '登录成功', 'token': new_token}, status=200)
                            else:
                                # Token过期或不正确
                                self.logger.warning(f'{self.request_path(request)} - Token过期或不正确')
                        else:
                            # Token未设置创建时间
                            self.logger.warning(f'{self.request_path(request)} - Token未设置创建时间')

                    # 尝试使用用户名和密码登录
                    login_sql = 'SELECT * FROM users WHERE userid=%s AND password=%s'
                    cursor.execute(login_sql, [userid, password])
                    login_result = cursor.fetchone()

                    if login_result:
                        new_token = self.create_uuid()
                        new_token_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        update_token_sql = 'UPDATE users SET token=%s, token_createtime=%s WHERE userid=%s'
                        cursor.execute(update_token_sql, [new_token, new_token_time, userid])
                        cursor.connection.commit()
                        print(f'{token}\t{new_token}\t用户名登录，token已更新')
                        return JsonResponse({'status': 'success', 'message': '登录成功', 'token': new_token},
                                            status=200)
                    else:
                        return JsonResponse({'status': 'failed', 'message': '用户名或密码错误'}, status=400)
                else:
                    return JsonResponse({'status': 'failed', 'message': '用户不存在'}, status=400)

        except json.JSONDecodeError as e:
            self.logger.error(f'{self.request_path(request)} - 访问失败：JSONDecodeError {str(e)}')
            return JsonResponse({'status': 'failed', 'message': '请求数据格式错误'}, status=400)

        except Exception as e:
            self.logger.error(
                f'{self.request_path(request)} - 访问失败：Exception {str(e)}，请求数据：{str(request.body)}')
            return JsonResponse({'status': 'failed', 'message': '服务器内部错误'}, status=500)


# 使用token获取用户信息
class UserInfoByToken(View):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger = Logger()

    def create_uuid(self):
        return str(uuid.uuid4())

    def request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR')
        return f'访问IP：{request_ip}，访问路径：{request_path}，时间：{self.now}'

    def get(self, request):
        self.logger.warning(f'{self.request_path(request)} - 访问失败：无效的请求方法')
        return JsonResponse({'status': 'failed', 'message': '无效的请求方法'}, status=400)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            token = data.get('token')
            if token:
                sql = 'select * from users where token=%s'
                with connection.cursor() as cursor:
                    cursor.execute(sql, [token])
                    result = cursor.fetchall()
                    if result:
                        columns = [desc[0] for desc in cursor.description]
                        rows = [dict(zip(columns, row)) for row in result]
                        # 删除密码
                        del rows[0]['password']
                        self.logger.info(f'{self.request_path(request)} - 访问成功')
                        return JsonResponse({'status': 'success', 'message': '获取用户信息成功', 'data': rows},
                                            status=200)
        except json.JSONDecodeError as e:
            self.logger.error(f'{self.request_path(request)} - 访问失败：JSONDecodeError {str(e)}')
            return JsonResponse({'status': 'failed', 'message': '请求数据格式错误'}, status=400)
        except Exception as e:
            print(e)
            self.logger.error(
                f'{self.request_path(request)} - 访问失败：Exception {str(e)}，请求数据：{str(request.body)}')
            return JsonResponse({'status': 'fail', 'message': '服务器错误'}, status=500)
