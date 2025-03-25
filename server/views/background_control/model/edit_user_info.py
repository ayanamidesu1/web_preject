from .authentication import Authentication
from django.db import connection
from django.views import View
from django.http import JsonResponse
from .log.log import Logger
from datetime import datetime
import json
from django.shortcuts import render


class EditUserInfo(View):
    authentication = Authentication()
    logger = Logger()

    def _request_path(self, request):
        request_path = request.path
        request_ip = request.META['REMOTE_ADDR']
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f'{request_ip}在{now}请求了{request_path}'

    def _log_and_return(self, request, level, message, data=None, status=200):
        log_message = f'{self._request_path(request)} {message}'
        if data:
            log_message += f'，请求数据为：{data}'
        getattr(self.logger, level)(log_message)
        return JsonResponse({'status': 'error', 'message': message}, status=status)

    def _get_user_info(self, cursor, userid):
        sql = '''
            SELECT username, user_avatar, user_address, password, user_back_img,
                   phone, email, user_self_website, sex, select_work, occupation,
                   birthday, vip, account_status, account_permissions
            FROM users
            WHERE userid = %s
        '''
        cursor.execute(sql, (userid,))
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        return dict(zip(columns, row)) if row else None

    def _update_user_info(self, cursor, user_data, userid, is_super_admin, target_user_permissions):
        update_fields = '''
            username = %(username)s, user_avatar = %(user_avatar)s, user_address = %(user_address)s, 
            password = %(password)s, user_back_img = %(user_back_img)s, phone = %(phone)s, 
            email = %(email)s, user_self_website = %(user_self_website)s, sex = %(sex)s, 
            select_work = %(select_work)s, occupation = %(occupation)s, birthday = %(birthday)s, 
            vip = %(vip)s, account_status = %(account_status)s
        '''
        # 只有在操作者为超级管理员且目标用户权限低于操作者时才允许更新权限字段
        if is_super_admin and target_user_permissions < 2:
            update_fields += ', account_permissions = %(account_permissions)s'

        sql = f'UPDATE users SET {update_fields} WHERE userid = %(userid)s'
        cursor.execute(sql, user_data)

    def get(self, request):
        self.logger.warning(self._request_path(request) + '非法GET请求，请求数据为：' + str(request.GET))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            operate_userid = str(getattr(request, 'userid', None))
            is_authenticated = getattr(request, 'is_authenticated', None)

            if is_authenticated is False:
                return JsonResponse({'status':'error','message':'用户未登录'},status=401)

            with connection.cursor() as cursor:
                # 获取操作者的权限
                cursor.execute('SELECT account_permissions FROM users WHERE userid=%s', (operate_userid,))
                account_permissions = int(cursor.fetchone()[0])

                if account_permissions is None:
                    return self._log_and_return(request, 'warning', '操作用户不存在')

                # 权值为0的用户直接返回权限不足
                if account_permissions == 0:
                    return self._log_and_return(request, 'warning', '权限不足', status=403)

                userid = data.get('userid')
                if not userid:
                    return self._log_and_return(request, 'warning', '缺少被操作用户的userid')

                user_info = self._get_user_info(cursor, userid)
                if not user_info:
                    return self._log_and_return(request, 'warning', '用户不存在')

                target_user_permissions = int(user_info['account_permissions'])

                # 权限检查：普通管理员不能操作比自己权限高或同级的用户
                if account_permissions == 1 and target_user_permissions >= account_permissions:
                    return self._log_and_return(request, 'warning', '权限不足，无法修改此用户的信息', status=403)

                # 防止用户修改自己的权限
                if operate_userid == userid or (account_permissions == 2 and target_user_permissions == 2):
                    data['account_permissions'] = target_user_permissions

                # 根据条件设置 account_permissions
                if int(data.get('account_permissions', target_user_permissions)) < 2:
                    data['account_permissions'] = data.get('account_permissions', target_user_permissions)
                else:
                    data['account_permissions'] = 0

                update_data = {
                    'userid': userid,
                    'username': data.get('username', user_info['username']),
                    'user_avatar': data.get('user_avatar', user_info['user_avatar']),
                    'user_address': data.get('user_address', user_info['user_address']),
                    'password': data.get('password', user_info['password']),
                    'user_back_img': data.get('user_back_img', user_info['user_back_img']),
                    'phone': data.get('phone', user_info['phone']),
                    'email': data.get('email', user_info['email']),
                    'user_self_website': data.get('user_self_website', user_info['user_self_website']),
                    'sex': data.get('sex', user_info['sex']),
                    'select_work': data.get('select_work', user_info['select_work']),
                    'occupation': data.get('occupation', user_info['occupation']),
                    'birthday': data.get('birthday', user_info['birthday']),
                    'vip': data.get('vip', user_info['vip']),
                    'account_status': data.get('account_status', user_info['account_status']),
                    'account_permissions': data['account_permissions'],
                    'current_userid': operate_userid
                }

                is_super_admin = account_permissions == 2

                if account_permissions>target_user_permissions:
                    self._update_user_info(cursor, update_data, userid, is_super_admin, target_user_permissions)
                else:
                    self._log_and_return(request, 'warning', '权限不足，无法修改此用户的信息', status=403)

                if is_super_admin:
                    self.logger.info(self._request_path(request) + '超级管理员修改用户信息，请求数据为：' + str(data))
                else:
                    self.logger.warning(
                        self._request_path(request) + '非超级管理员，修改用户信息，请求数据为：' + str(data))

                if cursor.rowcount >= 1:
                    return JsonResponse({'status': 'success', 'message': '修改成功'})
                else:
                    return self._log_and_return(request, 'warning', '没有修改任何信息', data)

        except Exception as e:
            print(e)
            return self._log_and_return(request, 'error', '服务器发生错误', str(e), status=500)
