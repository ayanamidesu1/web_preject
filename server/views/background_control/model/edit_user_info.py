from .authentication import Authentication
from django.db import connection
from django.views import View
from django.http import JsonResponse
from .log.log import Logger
from datetime import datetime
import json
from django.shortcuts import render
from base_api import BaseApi
#Django哈希密码生成
from django.contrib.auth.hashers import make_password, check_password


class EditUserInfo(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            # 权限验证（保持原有逻辑）
            if request.user.role not in ['admin', 'sys_admin'] and request.user.is_login is False:
                return JsonResponse({'code': 403, 'msg': '权限不足', 'status': 'error'}, status=403)

            data = self.format_request(request)
            userid = data.get('userid')
            operate_user_id = request.user.id

            # 参数校验（保持原有逻辑）
            if not userid:
                return JsonResponse({'code': 400, 'msg': '缺少userid', 'status': 'error'}, status=400)

            # 获取目标用户信息（保持原有逻辑）
            target_user_info = self.execute_sql(
                '''SELECT * FROM users WHERE userid=%s''',
                [userid]
            )[0]

            if not target_user_info:
                return JsonResponse({'code': 400, 'msg': '用户不存在', 'status': 'error'}, status=400)

            # 权限级别检查（保持原有逻辑）
            account_permissions = int(target_user_info.get('account_permissions', 0))
            operate_user_ac = 2 if request.user.role == 'sys_admin' else 1 if request.user.role == 'admin' else 0

            if account_permissions >= operate_user_ac:
                return JsonResponse({'code': 403, 'msg': '权限不足', 'status': 'error'}, status=403)

            # 构建更新数据（与旧接口相同的字段获取逻辑）
            update_fields = {
                'username': data.get('username', target_user_info['username']),
                'user_avatar': data.get('user_avatar', target_user_info['user_avatar']),
                'user_address': data.get('user_address', target_user_info['user_address']),
                'password': make_password(data.get('password')) if data.get('password') else target_user_info[
                    'password'],
                'user_back_img': data.get('user_back_img', target_user_info['user_back_img']),
                'phone': data.get('phone', target_user_info['phone']),
                'email': data.get('email', target_user_info['email']),
                'user_self_website': data.get('user_self_website', target_user_info['user_self_website']),
                'sex': data.get('sex', target_user_info['sex']),
                'select_work': data.get('select_work', target_user_info['select_work']),
                'occupation': data.get('occupation', target_user_info['occupation']),
                'birthday': data.get('birthday', target_user_info['birthday']),
                'vip': data.get('vip', target_user_info['vip']),
                'account_status': data.get('account_status', target_user_info['account_status']),
                'account_permissions': data.get('account_permissions', target_user_info['account_permissions'])
                if operate_user_ac == 2 else target_user_info['account_permissions']
            }

            # 动态生成更新SQL（保持与旧接口相同的安全更新方式）
            set_clause = ', '.join([f"{k}=%s" for k in update_fields.keys()])
            params = list(update_fields.values()) + [userid]

            affected_rows = self.execute_sql(
                f'''UPDATE users SET {set_clause} WHERE userid=%s''',
                params,
                False
            )

            if affected_rows == 1:
                return JsonResponse({'code': 200, 'msg': '修改成功', 'status': 'success'})
            return JsonResponse({'code': 500, 'msg': '更新失败', 'status': 'error'}, status=500)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误', 'status': 'error'}, status=500)



