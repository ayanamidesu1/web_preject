from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connect success')
        # 连接成功时向客户端发送消息
        await self.send(text_data=json.dumps({'message': 'Hello'}))
        await self.accept()

    async def disconnect(self, close_code):
        print('disconnect success')
        # 断开连接前向客户端发送消息
        await self.send(text_data=json.dumps({'message': 'Goodbye'}))

    async def receive(self, text_data):
        print('receive success')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 打印接收到的消息到控制台
        print(f"Received message from client: {message}")

        # 回复客户端收到的消息
        await self.send(text_data=json.dumps({
            'message': message
        }))
