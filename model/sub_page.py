import os
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.template
from model.login import do_select_query
import json

class sub_page(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(os.path.dirname(__file__), "../sub_page.html"))

class user_center(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(os.path.dirname(__file__), "../user_center.html"))

class ren:
    def make_app(self):
        return tornado.web.Application([
          (r"/sub_page", sub_page),
          (r"/user_center", user_center),
        ])

