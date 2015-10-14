#coding=utf-8
__author__ = 'knight'
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import psycopg2
import  psycopg2.extras

from tornado.options import define,options
define("port",default=8000,type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [((r"/(\w+)"),WordHandler)]
        conn = psycopg2.connect(database="test",port="5432",user="postgres",host="localhost",password="postgres")
        self.db = conn
        tornado.web.Application.__init__(self, handlers, debug=True)


class WordHandler(tornado.web.RequestHandler):
    def get(self,word):
        cursor = self.application.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from dict where word = %s",(word,))
        word_doc = cursor.fetchone()
        columns = ('id','word','definition')
        results = {}
        results = dict(zip(columns,word_doc))
        if word_doc:
            self.write(results)
        else:
            self.set_status(404)
            self.write({"error":"word not found"})

        cursor.close()

        
if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()