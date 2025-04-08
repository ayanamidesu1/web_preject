import json
from datetime import datetime
import jwt
import pymysql
import tornado
from tornado import httputil, web, websocket, httpclient
from tornado.ioloop import IOLoop
import sys
import os
from pathlib import Path

# 获取当前文件所在目录的绝对路径（tornado_server目录）
current_dir = Path(__file__).resolve().parent
# 计算项目根目录路径（H:\web_project\server）
server_dir = current_dir.parent
# 将server目录添加到Python路径
sys.path.append(str(server_dir))
# 现在可以正确导入djangoWebServer
from djangoWebServer.settings import BASE_DIR
import ssl
from base_connect import BaseConnect
from django_api import DjangoApi
from main_func import MainFunc


class ChatWebSocketHandler(BaseConnect,DjangoApi):
    #connected_users = {}  # 在线用户字典
    admin_id='f575b4d3-0683-11ef-adf4-00ffc6b98bdb'
    admin_connected_users = {} # 管理员连接池

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request)
        self.user_role = None
        self.user_id = None
        self.auth_token = None  # 存储用户的JWT token

    async def open(self):
        """异步处理连接建立"""
        # 1. 强制检查 WebSocket 协议头
        if self.request.headers.get("Upgrade", "").lower() != "websocket":
            await self.close(code=400, reason="Invalid protocol")
            return

        self.auth_token = self.get_argument("token")
        self.user_role=self.get_argument("role",'user')
        if self.user_role=='admin' or self.user_role=='sys_admin':
            self.user_id=self.get_argument('user_id')
            if self.user_id!='f575b4d3-0683-11ef-adf4-00ffc6b98bdb':
                await  self.close(code=4001, reason="非法管理员")
                return
            #将admin_id加入到连接池中
            if self.add_to_pool(self.user_id, role=self.user_role, pool_name='admin'):
                #通知管理员连接完成建立
                await self.write_message({'type': 'admin_connected', 'user_id': self.user_id})
                print("管理员连接成功")
                return
            else:
                print("管理员连接失败")
                return
        if not self.auth_token:
            await self.close(code=4001, reason="Missing authentication token")
            return

        try:
            user = self._decode_jwt()
            self.user_id = user.get("userid")

            # 验证用户有效性
            if not await self._validate_user():
                await self.close(code=4003, reason="User validation failed")
                return

            if self.add_to_pool(self.user_id, role=self.user_role, pool_name='default'):
                print("用户，连接成功")
            else:
                print("连接失败")
            await self.write_message({'status': 'connected'})

        except Exception as e:
            print(e)

    async def on_message(self, message):
        """异步处理消息（最简安全版）"""
        try:
            msg_data = self._parse_message(message)
            if not msg_data:
                print('空消息')
                return

            # 统一时间格式（解决datetime序列化问题）
            current_time = datetime.now().isoformat()

            if msg_data.get('type') == 'msg':
                # 单发消息（content保持原样）
                api_res = await self._store_message_via_api(msg_data)
                if api_res.code != 200:
                    print(f"存储失败: {api_res}")
                    await self._handle_api_error(api_res)
                else:
                    await self._forward_message(msg_data)

            elif msg_data.get('type') == 'heart_beat':
                print(f"心跳检测: {msg_data.get('target_user_id')}")
                await MainFunc.handle_heartbeat(self, msg_data)

            elif msg_data.get('type') == 'heart_beats':
                print(f"组心跳: {msg_data.get('target_user_ids')}")
                await MainFunc.handle_group_heartbeat(self, msg_data)

            elif msg_data.get('type') == 'group_msg':
                # 全局通知（自动处理content格式）
                content = msg_data.get('content')
                safe_msg = {
                    "msg_type": "all",
                    "content": json.loads(json.dumps(content)) if content else {},
                    "timestamp": current_time,
                    "time": current_time
                }
                self.send_to_group(safe_msg, pool_name='default')
                api_res = await self._store_message_via_api({
                    'target_user_id': 'all',
                    'content': content,
                    'chat_type': 'one_to_more',
                    'group_id': None,
                    'msg_type': 'all'
                })
                if api_res.code != 200:
                    print(f"通知存储失败: {api_res}")


            elif msg_data.get('type') == 'review_msg':
                content = msg_data.get('content', {})
                if not isinstance(content, dict):
                    content = {'error': 'Invalid content format'}
                # 确保 type 字段正确
                content['type'] = 'review_msg'
                # 发送实时消息（content 保持为字典）
                safe_msg = {
                    "msg_type": "review_msg",
                    "content": json.dumps(content),
                    "timestamp": current_time,
                    "time": current_time
                }
                self.send_to_user(msg_data.get('target_user_id'), safe_msg, pool_name='default')
                # 存储到数据库（序列化为 JSON 字符串）
                api_res = await self._store_message_via_api({
                    'target_user_id': msg_data.get('target_user_id'),
                    'content': json.dumps(content),  # 关键修正
                    'chat_type': 'one_to_one',
                    'group_id': None,
                    'msg_type': 'review_msg'
                })
                if api_res.code != 200:
                    print(f"审核存储失败: {api_res}")
            else:
                print(f"未知类型: {msg_data.get('type')}")

        except Exception as e:
            print(f"处理异常: {str(e)}")

    def _clean_dead_connection(self, user_id):
        """清理无效连接"""
        if user_id in self.connected_users:
            conn = self.connected_users[user_id]
            if conn.ws_connection is None or conn.ws_connection.is_closing():
                del self.connected_users[user_id]
                print(f"Cleaned dead connection: {user_id}")

    async def _forward_message(self, msg_data):
        """转发消息给接收方"""
        #receiver_conn = self.connected_users.get(msg_data['target_user_id'])
        r_conn=self.get_connection(msg_data['target_user_id'],pool_name='default', conn_type='conn')
        if r_conn:
            print("发送消息给接收方")
        formatted_msg = {
            'sender': self.user_id,
            'content': msg_data['content'],
            'timestamp': datetime.now().isoformat(),
            'message_id': self._generate_message_id()
        }

        #if receiver_conn:
            #await receiver_conn.write_message(formatted_msg)
            #await self.write_message({'status': 'delivered'})
        if r_conn:
            await r_conn.write_message(formatted_msg)
            await self.write_message({'status': 'delivered'})
        else:
            await self.write_message({'status': 'sent_offline'})

    def on_close(self):
        """改进连接关闭处理"""
        if self.user_id and self.user_id in self.connected_users:
            # 确保只移除当前实例
            if self.connected_users[self.user_id] == self:
                del self.connected_users[self.user_id]
                print(f"Connection removed → User: {self.user_id}, Remaining: {len(self.connected_users)}")
            else:
                print(f"Ignored stale connection removal for {self.user_id}")

    # 以下是辅助方法 -------------------------------------------------
    def _decode_jwt(self):
        """增加解码日志"""
        try:
            decoded = jwt.decode(
                self.auth_token,
                self.JWT_SECRET,
                algorithms=[self.JWT_ALGORITHM]
            )
            print(f"[JWT DECODE] Token decoded: {decoded}")
            return decoded
        except Exception as e:
            print(f"[JWT ERROR] Decode failed: {str(e)}")
            raise


    @staticmethod
    def _generate_message_id():
        """生成唯一消息ID（示例实现）"""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")

def make_app():
    return web.Application([
        (r'/chat', ChatWebSocketHandler),
    ])


if __name__ == "__main__":
    app = make_app()

    https_server = tornado.httpserver.HTTPServer(app, ssl_options={
        "certfile": os.path.join(BASE_DIR, "key", "server.crt"),
        "keyfile": os.path.join(BASE_DIR, "key", "server.key"),
    })
    https_server.listen(2234)

    print("Tornado WebSocket server is running on wss://localhost:2234/ws/chat")

    # 启动心跳广播，3秒一次
    tornado.ioloop.PeriodicCallback(
        ChatWebSocketHandler.broadcast_heartbeat,
        3000
    ).start()

    tornado.ioloop.IOLoop.current().start()
