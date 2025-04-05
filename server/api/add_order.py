from datetime import datetime

from base_api import BaseApi
from django.http import JsonResponse
import request
import os


class AddOrder(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录', 'data': None}, status=401)
            data = self.format_request(request)
            target_user_id = data.get('target_user_id')
            now = datetime.now()
            goods_id = self.get_uuid()
            sql = '''
            insert into order (type, amount_of_money, user_id, target_user_id, time, goods_id, status, work_type, 
            work_introduce, back, age_classification) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
            '''
            if self.execute_sql(sql, [data.get('type'), data.get('amount_of_money'), data.get('user_id'),
                                      target_user_id, now, goods_id, 3, data.get('work_type'),
                                      data.get('work_introduce'),
                                      data.get('back'), data.get('age_classification')], False) > 1:
                return JsonResponse({'code': 200, 'msg': '约稿成功', 'data': None}, status=200)
            else:
                return JsonResponse({'code': 400, 'msg': '约稿失败', 'data': None}, status=400)

        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({
                'code': 500,
                'msg': '服务器错误',
                'data': None
            }, status=500)

from django.conf import settings
import websocket
#建立wss连接向前端发送消息，同时消息存入数据库持久化
class NoticeUser:

    def __int__(self,target_user_id):
        self.target_user_id = target_user_id
        self.user_id = 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb'
        self.user_role = 'admin'
        self.server_ip = '''wss://127.0.0.1:2233/chat?role=admin
        &user_id=f575b4d3-0683-11ef-adf4-00ffc6b98bdb&target_user_id={}'''.format(self.target_user_id)
        key_path=os.path.join(settings.BASE_DIR,'server','key','server.key')
        crt_path=os.path.join(settings.BASE_DIR,'server','key','server.crt')
