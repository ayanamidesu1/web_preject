import json
from datetime import datetime
import jwt
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
from tornado import httputil, web, websocket, httpclient


class DjangoApi(websocket.WebSocketHandler):
    API_ENDPOINT = "https://www.sunyuanling.com/api/GetUserInfo/AddMsg"
    JWT_SECRET = "django-insecure-ypu2=#s5wqperumf6kmmi=eb4)u=#sror+nsa*kq$dfkhm7-a-"
    JWT_ALGORITHM = "HS256"

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

    async def _store_message_via_api(self, msg_data):
        """
        通过Django API存储消息
        Args:
            msg_data: 必须的消息格式为{
            target_user_id：目标用户ID，一对一时
            content：消息内容
            chat_type：one_to_one|one_to_more|more_to_more
            group_id:在群组内发送消息时
            }
        """

        http_client = httpclient.AsyncHTTPClient()
        body = {
            'target_user_id': msg_data.get('target_user_id'),
            'content': msg_data.get('content'),
            'chat_type': msg_data.get('chat_type'),
            'group_id': msg_data.get('group_id'),
            'msg_type':msg_data.get('msg_type', 'text')
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
            # 超时警告
            if res.code == 408:
                print("请求超时，请检查网络连接")
            print(f"API response: {res}")
            return res
        except httpclient.HTTPError as e:
            return e.response

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

    def _parse_message(self, raw_msg):
        """更健壮的消息解析"""
        if not raw_msg or not isinstance(raw_msg, str):
            print(f"无效消息内容: {repr(raw_msg)}")
            return None

        try:
            return json.loads(raw_msg)
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}\n原始消息: {raw_msg}")
            return None
        except Exception as e:
            print(f"消息处理异常: {e}")
            return None


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