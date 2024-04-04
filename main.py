import os
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.template
from model.connect_sqlsever import connMysql

# WebSocket 处理器
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket 连接已建立")

    def check_origin(self, origin):
        return True
    def on_message(self, message):
        print("收到消息：", message)
        self.write_message(f"你发送的消息是：{message}")

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

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", WSHandler),
        (r"/login_page", LoginHandler),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": "H:/web_preject/css"}),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": "H:/web_preject/js"}),
        (r"/image/(.*)",tornado.web.StaticFileHandler,{"path":"H:/web_preject/image"}),
    ])

if __name__ == "__main__":
    app = make_app()
    db_ipaddr = '127.0.0.1'
    db_name = 'web_user'
    db_username = 'root'
    db_password = 'root'

    conn = connMysql()
    conn.connect(db_ipaddr, db_name, db_username, db_password)
    app.listen(8888)
    print("服务器启动成功，请访问 http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
