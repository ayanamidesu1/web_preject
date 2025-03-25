from django.db import connection
from django.views import View
from django.http import JsonResponse
from ..log.log import Logger
import json
from datetime import datetime

class GroupControl(View):
    logger = Logger()

    def get(self, request, *args, **kwargs):
        now = datetime.now()
        request_path = self.get_request_path(request)
        self.logger.warning(f'时间：{now}，请求地址：{request_path}，'
                            f'请求方法：{request.method}，请求参数：{request.GET}，非法访问')
        return JsonResponse({'status': 'error', 'message': '非法访问'}, status=403)

    def post(self, request, *args, **kwargs):
        now = datetime.now()
        request_path = self.get_request_path(request)
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = data.get('userid')
            group_id = data.get('group_id')
            operation_request = data.get('operation_request')

            if not userid or not group_id or not operation_request:
                self.logger.error(f'时间：{now}，请求地址：{request_path}，'
                                  f'请求数据：{data}，缺少重要参数')
                return JsonResponse({'status': 'error', 'message': '缺少重要参数'}, status=400)

            with connection.cursor() as cursor:
                sql = 'SELECT role FROM `group` WHERE group_id = %s AND userid = %s'
                cursor.execute(sql, [group_id, userid])
                result = cursor.fetchone()

                if result:
                    role = result[0]
                    self.logger.info(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，用户角色：{role}')

                    if role == 'master':
                        return self.handle_master_operations(cursor, operation_request, data, now, request_path)
                    elif role == 'admin':
                        return self.handle_admin_operations(cursor, operation_request, data, now, request_path)
                    elif role == 'member':
                        return self.handle_member_operations(now, request_path)
                    else:
                        self.logger.error(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，未知角色')
                        return JsonResponse({'status': 'error', 'message': '未知角色'}, status=400)
                else:
                    self.logger.warning(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，'
                                        f'用户不在该群组中')
                    return JsonResponse({'status': 'error', 'message': '用户不在该群组中'}, status=403)

        except json.JSONDecodeError:
            self.logger.error(f'时间：{now}，请求地址：{request_path}，JSON解析错误')
            return JsonResponse({'status': 'error', 'message': 'JSON解析错误'}, status=400)
        except Exception as e:
            self.logger.error(f'时间：{now}，请求地址：{request_path}，服务器错误：{e}')
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)

    def handle_master_operations(self, cursor, operation_request, data, now, request_path):
        # 处理群主操作
        if operation_request == 'set_admin':
            return self.set_admin(cursor, data, now, request_path)
        elif operation_request == 'remove_member':
            return self.remove_member(cursor, data, now, request_path)
        elif operation_request == 'dissolve_group':
            return self.dissolve_group(cursor, data, now, request_path)
        elif operation_request == 'transfer_group':
            return self.transfer_group(cursor, data, now, request_path)
        else:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，非法操作请求：{operation_request}')
            return JsonResponse({'status': 'error', 'message': '非法操作请求'}, status=400)

    def handle_admin_operations(self, cursor, operation_request, data, now, request_path):
        # 处理管理员操作
        if operation_request == 'manage_members':
            return self.manage_members(cursor, data, now, request_path)
        else:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，非法操作请求：{operation_request}')
            return JsonResponse({'status': 'error', 'message': '非法操作请求'}, status=400)

    def handle_member_operations(self, now, request_path):
        # 成员没有特殊权限
        self.logger.warning(f'时间：{now}，请求地址：{request_path}，成员没有权限执行操作')
        return JsonResponse({'status': 'error', 'message': '没有权限执行操作'}, status=403)

    def set_admin(self, cursor, data, now, request_path):
        # 设置管理员
        group_id = data.get('group_id')
        userid = data.get('set_userid')
        userid_operator = data.get('userid_operator')
        if userid_operator == userid:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，不能设置自己为管理员')
            return JsonResponse({'status': 'error', 'message': '不能设置自己为管理员'}, status=403)
        sql = 'UPDATE `group` SET role = %s WHERE `group`.group_id = %s AND userid = %s'
        cursor.execute(sql, ['admin', group_id, userid])
        if cursor.rowcount > 0:
            self.logger.info(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，设置管理员成功')
            return JsonResponse({'status': 'success', 'message': '设置管理员成功'})
        else:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，设置管理员失败')
            return JsonResponse({'status': 'error', 'message': '设置管理员失败'}, status=400)

    def remove_member(self, cursor, data, now, request_path):
        # 移除成员
        group_id = data.get('group_id')
        userid = data.get('move_userid')
        userid_operator = data.get('userid_operator')
        if userid_operator == userid:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，不能移除自己')
            return JsonResponse({'status': 'error', 'message': '不能移除自己'}, status=403)
        sql = 'DELETE FROM `group` WHERE group_id = %s AND userid = %s'
        cursor.execute(sql, [group_id, userid])
        if cursor.rowcount > 0:
            self.logger.info(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，移除成员成功')
            return JsonResponse({'status': 'success', 'message': '移除成员成功'})
        else:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，移除成员失败')
            return JsonResponse({'status': 'error', 'message': '移除成员失败'}, status=400)

    def dissolve_group(self, cursor, data, now, request_path):
        # 解散群组
        group_id = data.get('group_id')
        sql = 'DELETE FROM `group` WHERE `group`.group_id = %s'
        cursor.execute(sql, [group_id])
        if cursor.rowcount > 0:
            self.logger.info(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，解散群组成功')
            return JsonResponse({'status': 'success', 'message': '解散群组成功'})
        else:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，解散群组失败')
            return JsonResponse({'status': 'error', 'message': '解散群组失败'}, status=400)

    def transfer_group(self, cursor, data, now, request_path):
        # 转移群组
        group_id = data.get('group_id')
        userid = data.get('transfer_userid')
        transfer_userid = data.get('userid')
        if transfer_userid == userid:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，不能转移群组给自己')
            return JsonResponse({'status': 'error', 'message': '不能转移群组给自己'}, status=403)
        sql = ('UPDATE `group` SET role = %s WHERE group_id = %s AND userid = %s;'
               'UPDATE `group` SET role = %s WHERE group_id = %s AND userid = %s')
        cursor.execute(sql, ['master', group_id, transfer_userid, 'admin', group_id, userid])
        if cursor.rowcount > 0:
            self.logger.info(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，转移群组成功')
            return JsonResponse({'status': 'success', 'message': '转移群组成功'})
        else:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，转移群组失败')
            return JsonResponse({'status': 'error', 'message': '转移群组失败'}, status=400)

    def manage_members(self, cursor, data, now, request_path):
        # 管理成员
        group_id = data.get('group_id')
        userid = data.get('move_userid')
        sql = 'SELECT userid FROM `group` WHERE group_id = %s AND role = %s'
        cursor.execute(sql, [group_id, 'master'])
        result = cursor.fetchone()
        if result is None:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，群组不存在或群组已被解散')
            return JsonResponse({'status': 'error', 'message': '群组不存在或群组已被解散'}, status=404)
        elif userid == result[0]:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，不能移除群主')
            return JsonResponse({'status': 'error', 'message': '操作非法，不能移除群主'}, status=403)
        userid_operator = data.get('userid_operator')
        if userid_operator == userid:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，不能移除自己')
            return JsonResponse({'status': 'error', 'message': '不能移除自己'}, status=403)
        sql = 'DELETE FROM `group` WHERE group_id = %s AND userid = %s'
        cursor.execute(sql, [group_id, userid])
        if cursor.rowcount > 0:
            self.logger.info(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，移除成员成功')
            return JsonResponse({'status': 'success', 'message': '移除成员成功'})
        else:
            self.logger.warning(f'时间：{now}，请求地址：{request_path}，请求数据：{data}，移除成员失败')
            return JsonResponse({'status': 'error', 'message': '移除成员失败'}, status=400)

    def get_request_path(self, request):
        # 请求来源IP地址
        ip_address = request.META.get('REMOTE_ADDR')
        request_path = request.path
        return f'{request_path} (IP: {ip_address})'
