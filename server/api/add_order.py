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
            amount = data.get('amount_of_money')

            if not target_user_id:
                return JsonResponse({'code': 400, 'msg': '缺少委托人ID', 'data': None}, status=400)
            if not amount:
                return JsonResponse({'code': 400, 'msg': '缺少金额', 'data': None}, status=400)

            amount = float(amount)

            # 查询当前用户余额
            balance_sql = '''SELECT balance FROM money WHERE user_id=%s'''
            result = self.execute_sql(balance_sql, [request.user.id], True)
            if not result:
                return JsonResponse({'code': 400, 'msg': '钱包不存在，请联系管理员', 'data': None}, status=400)

            current_balance = float(result[0].get('balance', 0))

            if current_balance < amount:
                return JsonResponse({'code': 402, 'msg': '余额不足，请充值后再试', 'data': None}, status=402)

            # 扣除余额
            now = datetime.now()
            update_balance_sql = '''UPDATE money SET balance=balance - %s, last_update=%s WHERE user_id=%s'''
            update_result = self.execute_sql(update_balance_sql, [amount, now, request.user.id], False)

            if update_result != 1:
                return JsonResponse({'code': 400, 'msg': '余额扣除失败，请重试', 'data': None}, status=400)

            # 创建订单
            goods_id = self.get_uuid()
            insert_sql = '''
            INSERT INTO `order` (type, amount_of_money, user_id, target_user_id, time, goods_id, status, work_type,
            work_introduce, back, age_classification) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

            insert_result = self.execute_sql(insert_sql, [
                'com_an_article', amount, request.user.id, target_user_id, now, goods_id, 3,
                data.get('work_type'), data.get('work_introduce'), data.get('back'), data.get('age_classification')
            ], False)

            if insert_result >= 1:
                # 发送通知
                notice = NoticeUser(target_user_id, {
                    'type': 'order_msg',
                    'content': '您有一条新的约稿消息，请注意到约稿中心中查看'
                })
                notice.send()

                return JsonResponse({'code': 200, 'msg': '约稿成功', 'data': None}, status=200)
            else:
                # 回滚余额？
                return JsonResponse({'code': 400, 'msg': '约稿失败，订单未创建', 'data': None}, status=400)

        except Exception as e:
            print("AddOrder 异常：", e)
            self.error_log(e, request)
            return JsonResponse({
                'code': 500,
                'msg': '服务器错误',
                'data': None
            }, status=500)


import websocket
import threading
import ssl
import json
import os
from django.conf import settings


class NoticeUser:
    def __init__(self, target_user_id, content: dict):
        self.target_user_id = target_user_id
        self.user_id = 'f575b4d3-0683-11ef-adf4-00ffc6b98bdb'
        self.user_role = 'admin'
        self.content = content
        self.ws_url = (
            f"wss://www.sunyuanling.com/ws/chat?role=admin"
            f"&user_id={self.user_id}&target_user_id={self.target_user_id}"
        )
        self.key_path = os.path.join(settings.BASE_DIR, 'server', 'key', 'server.key')
        self.crt_path = os.path.join(settings.BASE_DIR, 'server', 'key', 'server.crt')

    def _on_open(self, ws):
        msg = {
            "type": "order_msg",
            "target_user_id": self.target_user_id,
            "content": self.content
        }
        ws.send(json.dumps(msg))
        ws.close()

    def _on_error(self, ws, error):
        print("WebSocket 错误:", error)

    def _on_close(self, ws, close_status_code, close_msg):
        print("连接关闭", close_status_code, close_msg)

    def send(self):
        def run():
            ws = websocket.WebSocketApp(
                self.ws_url,
                on_open=self._on_open,
                on_error=self._on_error,
                on_close=self._on_close
            )
            ws.run_forever(sslopt={
                "certfile": self.crt_path,
                "keyfile": self.key_path,
                "cert_reqs": ssl.CERT_NONE
            })

        thread = threading.Thread(target=run)
        thread.start()
