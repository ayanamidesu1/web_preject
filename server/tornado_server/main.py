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


class ChatWebSocketHandler(websocket.WebSocketHandler):
    connected_users = {}  # 在线用户字典
    API_ENDPOINT = "https://www.sunyuanling.com/api/GetUserInfo/AddMsg"
    JWT_SECRET = "django-insecure-ypu2=#s5wqperumf6kmmi=eb4)u=#sror+nsa*kq$dfkhm7-a-"
    JWT_ALGORITHM = "HS256"

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request)
        self.user_id = None
        self.auth_token = None  # 存储用户的JWT token

    def check_origin(self, origin):
        return True

    async def open(self):
        """异步处理连接建立"""
        self.auth_token = self.get_argument("token")
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

            self._add_to_connection_pool()
            await self.write_message({'status': 'connected'})

        except Exception as e:
            print(e)
            await self.handle_auth_error(e)

    async def on_message(self, message):
        """异步处理消息"""
        try:
            msg_data = self._parse_message(message)
            print(f"Received message: {msg_data}")
            if not msg_data:
                print('没有消息')
                return
            if msg_data.get('type')=='msg':
                # 通过Django API存储消息
                print("向Django服务器发送请求到Django服务器...，{}".format(msg_data))
                api_response = await self._store_message_via_api(msg_data)

                if api_response.code != 200:
                    print("消息存储失败，失败原因：{}".format(api_response))
                    await self._handle_api_error(api_response)
                    return

                # 转发消息给接收方
                print("转发消息给接收方...")
                await self._forward_message(msg_data)
            if msg_data.get('type')=='heart_beat':
                target_user_id=msg_data.get('target_user_id')
                print("建立目标用户心跳")
                await self._handle_heartbeat(msg_data)
            if msg_data.get('type')=='heart_beats':
                target_user_ids=msg_data.get('target_user_ids')
                print("建立目标组心跳")
                await self._handle_group_heartbeat(msg_data)

        except Exception as e:
            print(e)

    async def _handle_heartbeat(self, msg_data):
        """处理一对一心跳"""
        try:
            target_id = msg_data.get('target_user_id')
            if not target_id:
                print("Missing target ID in heartbeat")
                return

            # 发送心跳响应
            await self.write_message({
                'type': 'heartbeat_ack',
                'from_user': self.user_id,
                'timestamp': datetime.now().isoformat()
            })

            # 可选：验证对方在线状态
            if target_id in self.connected_users:
                try:
                    # 发送双向心跳确认
                    await self.connected_users[target_id].write_message({
                        'type': 'heartbeat_notify',
                        'from_user': self.user_id,
                        'timestamp': datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Heartbeat failed to {target_id}: {str(e)}")
                    self._clean_dead_connection(target_id)

        except Exception as e:
            print(f"Heartbeat handling error: {str(e)}")

    async def _handle_group_heartbeat(self, msg_data):
        """处理群组心跳"""
        try:
            target_ids = msg_data.get('target_user_ids', [])
            valid_connections = []

            # 筛选有效连接
            for uid in target_ids:
                conn = self.connected_users.get(uid)
                if conn and conn.ws_connection and not conn.ws_connection.is_closing():
                    valid_connections.append(conn)
                else:
                    self._clean_dead_connection(uid)

            # 批量发送心跳响应
            responses = []
            for conn in valid_connections:
                try:
                    await conn.write_message({
                        'type': 'group_heartbeat_ack',
                        'from_user': self.user_id,
                        'timestamp': datetime.now().isoformat()
                    })
                    responses.append(True)
                except:
                    responses.append(False)

            # 返回统计结果
            await self.write_message({
                'type': 'heartbeat_summary',
                'total': len(responses),
                'success': sum(responses),
                'failed': len(responses) - sum(responses)
            })

        except Exception as e:
            print(f"Group heartbeat error: {str(e)}")

    def _clean_dead_connection(self, user_id):
        """清理无效连接"""
        if user_id in self.connected_users:
            conn = self.connected_users[user_id]
            if conn.ws_connection is None or conn.ws_connection.is_closing():
                del self.connected_users[user_id]
                print(f"Cleaned dead connection: {user_id}")

    async def _forward_message(self, msg_data):
        """转发消息给接收方"""
        receiver_conn = self.connected_users.get(msg_data['target_user_id'])
        formatted_msg = {
            'sender': self.user_id,
            'content': msg_data['content'],
            'timestamp': datetime.now().isoformat(),
            'message_id': self._generate_message_id()
        }

        if receiver_conn:
            await receiver_conn.write_message(formatted_msg)
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

    async def _validate_user(self):
        """验证用户有效性"""
        try:
            http_client = httpclient.AsyncHTTPClient()
            response = await http_client.fetch(
                "https://www.sunyuanling.com/api/verify/",
                method="POST",
                headers={"Authorization": f"token {self.auth_token}"},
                body="",
                ssl_options=ssl._create_unverified_context()
            )
            print(f"Validation response: {response}")
            return response.code == 200
        except httpclient.HTTPError as e:
            print(f"Validation failed: {e}")
            return False

    def _add_to_connection_pool(self):
        """添加到连接池"""
        if self.user_id in self.connected_users:
            old_conn = self.connected_users[self.user_id]
            old_conn.close(code=4002, reason="New connection from same user")

        self.connected_users[self.user_id] = self
        print(f"User {self.user_id} connected. Total: {len(self.connected_users)}")

    def _parse_message(self, raw_msg):
        """解析原始消息"""
        try:
            data = json.loads(raw_msg)
            return {
                'target_user_id': data.get('target_user_id'),
                'content': data.get('content'),
                'chat_type': data.get('chat_type', 'one_to_one'),
                'group_id': data.get('group_id'),
                'type':data.get('type'),
                'target_user_ids': data.get('target_user_ids')
            }
        except (json.JSONDecodeError, KeyError) as e:
            print(e)

    async def _store_message_via_api(self, msg_data):
        """通过Django API存储消息"""
        http_client = httpclient.AsyncHTTPClient()
        body = {
            'target_user_id': msg_data['target_user_id'],
            'content': msg_data['content'],
            'chat_type': msg_data['chat_type'],
            'group_id': msg_data['group_id']
        }
        print("向Django服务器发送请求到Django服务器...，{}".format(body))
        try:
            res = await http_client.fetch(
                'https://www.sunyuanling.com/api/GetUserInfo/AddMsg',
                method="POST",
                headers={
                    "Authorization": f"token {self.auth_token}",
                    "Content-Type": "application/json"
                },
                body=json.dumps(body),
                ssl_options=ssl._create_unverified_context(),
                request_timeout=3
            )
            #超时警告
            if res.code == 408:
                print("请求超时，请检查网络连接")
            print(f"API response: {res}")
            return res
        except httpclient.HTTPError as e:
            return e.response

    async def _handle_api_error(self, response):
        """处理API错误响应"""
        try:
            error_data = json.loads(response.body)
            await self.write_message({
                'error': 'api_error',
                'code': error_data.get('code', 500),
                'message': error_data.get('msg', 'Unknown API error')
            })
        except json.JSONDecodeError:
            await self.write_message({
                'error': 'api_communication_failed',
                'details': f"HTTP {response.code}: {response.body.decode()}"
            })

    @staticmethod
    def _generate_message_id():
        """生成唯一消息ID（示例实现）"""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")

    #广播用户心跳
    @staticmethod
    def broadcast_heartbeat():
        heartbeat_msg = json.dumps({'heartbeat': datetime.now().isoformat()})
        for user_id, conn in ChatWebSocketHandler.connected_users.items():
            try:
                conn.write_message(heartbeat_msg)
            except Exception as e:
                print(f"Failed to send heartbeat to {user_id}: {e}")


def make_app():
    return web.Application([
        (r'/chat', ChatWebSocketHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    certfile = os.path.join(BASE_DIR, "key", "server.crt")
    keyfile = os.path.join(BASE_DIR, "key", "server.key")
    print(certfile)
    print(keyfile)
    https_server = tornado.httpserver.HTTPServer(app, ssl_options={
        "certfile": certfile,
        "keyfile": keyfile,
    })
    https_server.listen(2234)
    print("Tornado WebSocket server is running on wss://localhost:2234/ws/chat")
    #启动心跳广播，3s广播一次
    tornado.ioloop.PeriodicCallback(ChatWebSocketHandler.broadcast_heartbeat, 3000).start()

    tornado.ioloop.IOLoop.current().start()
