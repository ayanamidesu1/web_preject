import json
import uuid
from datetime import datetime, timedelta

from django.views import View
from django.http import JsonResponse
from django.db import connection

from ..log.log import Logger


class Login(View):
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
            token=getattr(request, 'token', None)
            if token:
                print('从请求头中获取的token'+str(token))
                return JsonResponse({'status': 'success', 'message': '登录成功', 'token': token}, status=200)
            else:
                print('从请求头中获取的token为空')
                return JsonResponse({'status': 'failed', 'message': 'token为空'}, status=400)
        except Exception as e:
            print(e)
            '''data = json.loads(request.body.decode('utf-8'))
            userid = data.get('userid')
            username=data.get('username')
            password = data.get('password')
            token = data.get('token')
            cookies_token=request.COOKIES

            token_sql = 'SELECT * FROM users WHERE username=%s or userid=%s OR token=%s'

            with connection.cursor() as cursor:
                cursor.execute(token_sql, [username,userid, token])
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
                                print('从请求连接中获取的cookies'+str(cookies_token))
                                return JsonResponse(
                                    {'status': 'success', 'message': '登录成功', 'token': new_token}, status=200)
                            else:
                                # Token过期或不正确
                                self.logger.warning(f'{self.request_path(request)} - Token过期或不正确')
                        else:
                            # Token未设置创建时间
                            self.logger.warning(f'{self.request_path(request)} - Token未设置创建时间')

                    # 尝试使用用户名和密码登录
                    login_sql = 'SELECT * FROM users WHERE userid=%s or username=%s AND password=%s'
                    cursor.execute(login_sql, [userid,username, password])
                    login_result = cursor.fetchone()

                    if login_result:
                        new_token = self.create_uuid()
                        new_token_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        update_token_sql = 'UPDATE users SET token=%s, token_createtime=%s WHERE userid=%s or username=%s'
                        cursor.execute(update_token_sql, [new_token, new_token_time, userid,username])
                        cursor.connection.commit()
                        print(f'{token}\t{new_token}\t用户名登录，token已更新')
                        return JsonResponse({'status': 'success', 'message': '登录成功', 'token': new_token},
                                            status=200)
                    else:
                        print('用户名或密码错误')
                        return JsonResponse({'status': 'failed', 'message': '用户名或密码错误'}, status=400)
                else:
                    print('token用户不存在')
                    return JsonResponse({'status': 'failed', 'message': '用户不存在'}, status=400)

        except json.JSONDecodeError as e:
            self.logger.error(f'{self.request_path(request)} - 访问失败：JSONDecodeError {str(e)}')
            print(e)
            return JsonResponse({'status': 'failed', 'message': '请求数据格式错误'}, status=400)

        except Exception as e:
            self.logger.error(
                f'{self.request_path(request)} - 访问失败：Exception {str(e)}，请求数据：{str(request.body)}')
            print(e)
            return JsonResponse({'status': 'failed', 'message': '服务器内部错误'}, status=500)
            '''
