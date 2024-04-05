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



class FileUploadHandler(tornado.web.RequestHandler):
    UPLOAD_DIR = "user_uploadavatar"
    def get(self):
        self.render("register.html")
    def post(self):
        # 检查是否有文件上传
        if 'file' in self.request.files:
            file_info = self.request.files['file'][0]
            fname = file_info['filename']
            content_type = file_info['content_type']
            body = file_info['body']

            # 确保上传目录存在
            if not os.path.exists(self.UPLOAD_DIR):
                os.makedirs(self.UPLOAD_DIR)

            # 构建保存文件的路径
            upload_path = os.path.join(self.UPLOAD_DIR, fname)

            # 保存文件
            with open(upload_path, 'wb') as f:
                f.write(body)

            # 返回成功信息给客户端
            self.write("文件上传成功")
        else:
            self.write("没有上传文件")



def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", WSHandler),
        (r"/login_page", LoginHandler),
        (r"/sub_page", subpageHandler),
        (r"/register",FileUploadHandler),
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
