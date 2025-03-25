from django.http import JsonResponse
from django.views import View
from datetime import datetime
from .log.log import Logger
import json
from .authentication import Authentication
from django.shortcuts import render
from django.db import connection

class AdminLogin(View):
    logger = Logger()
    authentication = Authentication()

    def _request_path(self, request):
        request_path = request.path
        request_ip = request.META.get('REMOTE_ADDR', '未知')
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        return f'{request_ip} 在 {now} 访问了 {request_path}'

    def get(self, request):
        self.logger.warning(f"{self._request_path(request)} 非法 GET 请求，请求数据为：{request.GET}")
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            userid = str(getattr(request, 'userid', None))
            token = str(getattr(request, 'token', None))
            is_authenticated = getattr(request, 'is_authenticated', False)
            userinfo = str(getattr(request, 'userinfo', None))

            if is_authenticated:
                # 确保 userinfo 是一个字典或可序列化对象
                print('userinfo:', userinfo)
                if isinstance(userinfo, bytes):
                    userinfo = json.loads(userinfo.decode('utf-8'))  # 将 bytes 解码并转换为字典
                sql='''select * from users where userid=%s'''
                with connection.cursor() as cursor:
                    cursor.execute(sql, (userid,))
                    userinfo=cursor.fetchone()
                    columns = [col[0] for col in cursor.description]
                    userinfo = dict(zip(columns, userinfo))
                    fields_to_remove = {'password', 'token', 'ip_address', 'user_register', 'last_login', 'phone'}
                    for field in fields_to_remove:
                        userinfo.pop(field, None)
                return JsonResponse({
                    'status': 'success',
                    'token': token,
                    'user_info': userinfo,  # 直接传递 userinfo 字典
                    'userid': userid,
                    'is_login':1
                })
            else:
                return JsonResponse({'status': 'error', 'message': '用户未登录','is_login':0}, status=401)

        except json.JSONDecodeError as e:
            self.logger.error(f"{self._request_path(request)} 请求数据解析失败，数据为：{request.body.decode('utf-8')}")
            return JsonResponse({'status': 'error', 'message': '请求数据解析失败'}, status=400)
        except Exception as e:
            print('\nadmin_login类错误', e)
            self.logger.error(f"{self._request_path(request)} 请求数据为：{request.body.decode('utf-8')}，错误信息为：{e}")
            return JsonResponse({'status': 'error', 'message': '服务器错误'}, status=500)


