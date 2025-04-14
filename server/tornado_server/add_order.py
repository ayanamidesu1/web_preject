# tornado_handlers/add_order.py
import json
import ssl
from typing import Any

import pymysql
import uuid
from datetime import datetime

from aiohttp.abc import Application
from tornado import httputil
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient, HTTPError
from base_connect import BaseConnect  # 只用它的 send_to_user 功能


class TornadoAddOrderHandler(RequestHandler, BaseConnect):
    def __init__(
            self,
            application: "Application",
            request: httputil.HTTPServerRequest,
            **kwargs: Any,
    ):
        super().__init__(application, request, kwargs)
        self.cursor = None
        self.db = None
        self.auth_token = None

    def initialize(self):
        self.db = pymysql.connect(
            host='localhost',
            user='admin',
            password='123456',
            db='admin',
            port=3306,
            charset='utf8mb4'
        )
        self.cursor = self.db.cursor()

    async def prepare(self):
        """Header 鉴权"""
        self.auth_token = self.request.headers.get("Authorization")
        if not self.auth_token:
            self.set_status(401)
            await  self.finish({"msg": "未登录"})
            return

        try:
            client = AsyncHTTPClient()
            res = await client.fetch(
                "https://www.sunyuanling.com/api/verify/",
                method="POST",
                headers={"Authorization":f"token {self.auth_token}"},
                body="",
                ssl_options=ssl._create_unverified_context()
            )
            if res.code != 200:
                self.set_status(403)
                await  self.finish({"msg": "认证失败"})
        except HTTPError as e:
            print(e)
            self.set_status(403)
            await self.finish({"msg": "认证异常", "detail": str(e)})

    async def post(self):
        try:
            data = json.loads(self.request.body.decode())
            now = datetime.now()
            goods_id = str(uuid.uuid4())

            sql = '''
            INSERT INTO `order` (type, amount_of_money, user_id, target_user_id, time, goods_id, status, work_type, 
            work_introduce, back, age_classification) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            values = [
                data.get("type"),
                data.get("amount_of_money"),
                data.get("user_id"),
                data.get("target_user_id"),
                now,
                goods_id,
                3,
                data.get("work_type"),
                data.get("work_introduce"),
                data.get("back"),
                data.get("age_classification")
            ]

            self.cursor.execute(sql, values)
            self.db.commit()

            # 发送推送消息
            message = {
                "type": "new_order",
                "msg": "你有一个新约稿，请注意查看约稿管理以确认是否接受该约稿请求。",
                "from": data.get("user_id"),
                "time": now.strftime("%Y-%m-%d %H:%M:%S")
            }

            self.send_to_user(data.get("target_user_id"), message)

            await self.finish({"code": 200, "msg": "订单创建成功"})
        except Exception as e:
            print(e)
            self.set_status(500)
            await  self.finish({"code": 500, "msg": "服务器错误", "error": str(e)})

    def on_finish(self):
        """清理连接"""
        if hasattr(self, "cursor"):
            self.cursor.close()
        if hasattr(self, "db"):
            self.db.close()
