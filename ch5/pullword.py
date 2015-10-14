#coding=utf-8
__author__ = 'knight'
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import  tornado.httpclient

import urllib
import json
import datetime
import  time

from tornado.options import define,options
define("port",default=8000,help="run on the given port",type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        source = self.get_argument("source")
        