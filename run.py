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
from datetime import datetime
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
    document.pop("create_time")
    return document

class ErrorHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode(encoding="UTF-8"))
        data["create_time"] = datetime.now()
        print("error", data)
        db.error_log.insert(data)
        self.write({})

class LogHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode(encoding="UTF-8"))
        data["create_time"] = datetime.now()
        db.log.insert(data)
        self.write({})

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "JSNLog-RequestId,Accept,Origin,Content-Type,X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Credentials", "true")

class UsersHandler(tornado.web.RequestHandler):
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
        def check_properties(obj, case):
            if(case == "profile_image"):
                try:
                    result = data["properties"]["profile_image"]
                except KeyError as e:
                    return None
            elif(case == "thumbnail_image"):
                try:
                    result = data["properties"]["thumbnail_image"]
                except KeyError as e:
                    return None
            elif(case == "nickname"):
                try:
                    result = data["properties"]["nickname"]
                except KeyError as e:
                    return None
            elif(case == "latitude"):
                try:
                    result = data["latitude"]
                except KeyError as e:
                    return 37.510531
            elif(case == "longitude"):
                try:
                    result = data["longitude"]
                except KeyError as e:
                    return 126.988538
            elif(case == "userAgent"):
                try:
                    result = data["userAgent"]
                except KeyError as e:
                    return None
            else:
                return None
            return result

        new_one = {
            "kakao_id": user_id,
            "profile_image": check_properties(data, "profile_image"),
            "thumbnail_image": check_properties(data, "thumbnail_image"),
            "nickname": check_properties(data, "nickname"),
            "latitude": check_properties(data, "latitude"),
            "longitude": check_properties(data, "longitude"),
            "user_agent": check_properties(data, "userAgent"),
            "create_time": datetime.now()
            }

        db.users.find_and_modify({"kakao_id":user_id}, {"$set":new_one}, new=True)
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
            (r"/error", ErrorHandler),
            (r"/log", LogHandler),
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
