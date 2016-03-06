# -*- coding:utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
import tornado.options
import tornado.gen
import os
import pymongo
import operator
import json
import sys
import time
import socket
import logging
from platform import system
from tornado.options import define, options
from tornado import gen
from pymongo import MongoClient

GLOBALS = {"db_name":"whereIsMyFriend"}
dirname = os.path.dirname(__file__)
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db'))
STATIC_PATH = os.path.join(dirname, 'www')

define("port", default=8000, help="run on the given port", type=int)
client = MongoClient('127.0.0.1', 27017)
db = client[GLOBALS["db_name"]]

def remove_object_id(document):
    document.pop("_id")
    return document

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "JSNLog-RequestId,Accept,Origin,Content-Type,X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Credentials", "true")

class UsersHandler(BaseHandler):
    def get(self):
        users_c = db.users.find()
        users = [remove_object_id(u) for u in users_c]
        self.write({"result":users})

class UserHandler(tornado.web.RequestHandler):
    def get(self, user_id):
        pass

    # @tornado.web.asynchronous
    def post(self, user_id):
        data = json.loads(self.request.body.decode(encoding="UTF-8"))
        user_c = db.users.find_one({"kakao_id":user_id})
        if user_c is None:
            db.users.insert({
                "kakao_id": user_id,
                "profile_image": data["properties"]["profile_image"],
                "thumbnail_image": data["properties"]["thumbnail_image"],
                "nickname": data["properties"]["nickname"],
                "latitude": data["latitude"],
                "longitutde": data["longitude"]
            })
        self.write({})

    # def _on_response(self, result, error):
    #     print("response ", result, error)
    #     if error:
    #         pass
    #     else:
    #         self.finish()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/users", UsersHandler),
            (r"/users/(.*)", UserHandler),
            (r"/()$", tornado.web.StaticFileHandler, {'path': 'www/index.html'}),
            (r"/(.*)", tornado.web.StaticFileHandler, {'path':'www/'})
        ]
        settings = {
            "static_path": STATIC_PATH,
            "debug" : True
        }
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    args = sys.argv
    cur_sys = system()
    file_name = GLOBALS["db_name"]+"-"+str(options.port)+".log"
    # if cur_sys == "Darwin":
    #     f = "/Users/"+os.getlogin()+"/Desktop/"+ file_name
    # elif cur_sys == "Linux":
    #     f = os.getcwd() + "/" + file_name
    # else:
    #     raise NotImplementedError
    # args.append("--log_file_prefix=" + f)
    # logging.basicConfig(filename=f, level=logging.DEBUG)

    tornado.options.parse_command_line()
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton, xheaders=True)

    http_server.listen(options.port)
    print("="*50)
    print("initializing program with port : ", options.port)
    print("="*50)
    print("my ip is : ", socket.gethostbyname(socket.gethostname()))
    print("="*50)
    print("File system DEFAULT Encoding-type is : ", sys.getdefaultencoding())
    print("File system Encoding-type is : ", sys.getfilesystemencoding())
    print("="*50)
    logging.info("File system DEFAULT Encoding-type is : " + str(sys.getdefaultencoding()))
    logging.info("File system Encoding-type is : " +  str(sys.getfilesystemencoding()))

    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()

if __name__ == "__main__":
    main()
