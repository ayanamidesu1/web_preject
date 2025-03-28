import json
from datetime import datetime
from typing import Any

import jwt
import pymysql
from pymysql import DatabaseError
import tornado
from tornado import httputil

from WebSocketHandler import WebSocketHandler
import tornado.websocket
from operate_db import OperateDB

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'forum',
    'password': '123456',
    'db': 'forum',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

class DefaultHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        """设置默认的 CORS 头"""
        self.set_header("Access-Control-Allow-Origin", "*")  # 允许所有来源
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def options(self):
        """处理预检请求（OPTIONS）"""
        self.set_status(204)
        self.finish()

    def get(self):
        self.write("hello world")
class TestWebSocketHandler(tornado.websocket.WebSocketHandler):
    # 使用字典存储在线用户：键为 user_id，值为 WebSocket 实例
    connected_users = {}

    def __init__(self, application: tornado.web.Application, request: httputil.HTTPServerRequest, **kwargs):
        super().__init__(application, request)
        self.user_id = None

    def check_origin(self, origin):
        return True  # 允许所有来源

    def open(self):
        """连接建立时验证用户身份并加入连接池"""
        token = self.get_argument("token", default=None)
        if not token:
            self.close(code=4001, reason="Missing token")
            print("Missing token")
            return

        try:
            # 解析 JWT 并获取用户信息
            user = self.decode_jwt(token)
            user_id = user.get("user_id")
            self.user_id = user_id  # 存储到实例属性

            # 将当前用户加入连接池
            self.__class__.connected_users[user_id] = self
            print(f"User {user_id} connected. Total users: {len(self.connected_users)}")
            print("Connected users:", self.connected_users)

            # 发送欢迎消息
            self.write_message({'hello':'connect websocket'})
        except Exception as e:
            self.close(code=4000, reason=str(e))

    def on_message(self, message):
        try:
            data = json.loads(message)
            target_user_id = data.get("target_user_id")
            raw_msg = data.get("msg")

            # 确保 msg 是字典
            if isinstance(raw_msg, str):
                msg = {
                    'content': raw_msg,
                    'send_user_id': self.user_id,
                    'receiver_id': target_user_id
                }
            else:
                msg = raw_msg
                msg['send_user_id'] = self.user_id
                msg['receiver_id'] = target_user_id

            now = datetime.now()
            print(f"Received from {self.user_id} to {target_user_id}: {msg}")

            # 插入数据库
            sql = "INSERT INTO messages (sender_id, receiver_id, content, send_time, is_read) VALUES (%s, %s, %s, %s, %s)"
            self.insert_sql(sql, [
                self.user_id,
                target_user_id,
                msg.get('content', raw_msg),
                now,
                0
            ])

            # 发送确认
            self.write_message({'reply_msg': msg})

            # 发送给目标用户
            target = self.__class__.connected_users.get(target_user_id)
            if target:
                target.write_message({'msg': msg})
            else:
                self.write_message(f"User {target_user_id} offline")
        except Exception as e:
            self.write_message(f"Error: {str(e)}")

    def on_close(self):
        """连接关闭时移除用户"""
        if self.user_id in self.__class__.connected_users:
            del self.__class__.connected_users[self.user_id]
            print(f"User {self.user_id} disconnected. Total users: {len(self.connected_users)}")

    def decode_jwt(self, token):
        """解码 JWT 令牌，返回解码后的 payload 或 None"""
        KEY = 'django-insecure-pm__s5rkwbf1#=l!j4%uh*hy5)3g!ld6_cod&e(o!yx)7#=)^z'
        JWT_ALGORITHM = 'HS256'
        try:
            return jwt.decode(token, KEY, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            self.write({"code": 401, "msg": "令牌已过期"})
            return None
        except jwt.InvalidTokenError:
            self.write({"code": 401, "msg": "无效的令牌"})
            return None
    def insert_sql(self, sql, params=None):
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
            connection.commit()
            return True
        except DatabaseError as e:
            connection.rollback()
            print(f"Error executing SQL: {e}")
            return False
        finally:
            connection.close()

if __name__ == '__main__':
   app=tornado.web.Application([
       (r'/', DefaultHandler),
       (r'/ws',WebSocketHandler),
       (r'/ts',TestWebSocketHandler)
   ])
   print('监听2233端口')
   app.listen(2233)
   tornado.ioloop.IOLoop.current().start()





