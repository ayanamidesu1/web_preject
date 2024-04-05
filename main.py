import os
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.template
from model.connect_sqlsever import connMysql
from model.login import do_select_query
import json


# WebSocket 处理器
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket 连接已建立")

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        print("收到消息：", message)
        # 在这里处理用户信息
        userinfo = json.loads(message)
        print(userinfo['username'])
        print(userinfo['password'])
        conn = do_select_query()
        conn.conn()
        # 构造 SQL 查询语句，并执行查询
        sql_query = f"select username, password from user_table where username='{userinfo['username']}' and password='{userinfo['password']}'"
        result = conn.select_query(sql_query)
        print(len(result))
        print(result[0])
        if result and len(result) > 2:
            print(result)
            response = {"status": "success", "message": "登录成功"}
        else:
            response = {"status": "error", "message": "用户名或密码错误"}
        # 将查询结果发送回客户端
        self.write_message(json.dumps(response))

    def on_close(self):
        print("WebSocket 连接已关闭")


# 主页面处理器
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("index.html").generate())


# 登录页面处理器
class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")


class subpageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("artwork/1111.html")


class registerHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("register.html")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", WSHandler),
        (r"/login_page", LoginHandler),
        (r"/sub_page", subpageHandler),
        (r"/artwork/(.*)", tornado.web.StaticFileHandler, {"path": "H:/web_preject/artwork"}),
        (r"/artwork_js/(.*)", tornado.web.StaticFileHandler, {"path": "H:/web_preject/artwork/artwork_js"}),
        (r"/artwork_css/(.*)", tornado.web.StaticFileHandler, {"path": "H:/web_preject/artwork/artwork_css"}),
        (r"/image/(.*)", tornado.web.StaticFileHandler, {"path": "H:/web_preject/artwork/image"}),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": "H:/web_preject/css"}),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": "H:/web_preject/js"}),
        (r"/image/(.*)", tornado.web.StaticFileHandler, {"path": "H:/web_preject/image"}),
        (r"/user_uploadavatar/(.*)", tornado.web.StaticFileHandler, {"path": "H:/web_preject/user_uploadavatar"}),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("服务器启动成功，请访问 http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
