#coding=utf-8
# __author__ = 'knight'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import psycopg2
import psycopg2.extras

from tornado.options import define,options
define("port",default=8000,help="run on the given port",type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/(\w+)",WordHandler)]
        conn = psycopg2.connect(database="test",port="5432",user="postgres",host="localhost",password="postgres")
        self.db = conn
        tornado.web.Application.__init__(self, handlers, debug=True)

class WordHandler(tornado.web.RequestHandler):
    def get(self,word):
        cursor = self.application.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from dict where word = %s",(word,))
        word_doc = cursor.fetchone()
        if word_doc:
            columns = ('id','word','definition')
            results = dict(zip(columns,word_doc))
            self.write(results)
        else:
            self.set_status(404)

        cursor.close()
        self.application.db.commit()

    def post(self,word):
        definition = self.get_argument("definition")
        cursor = self.application.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("select * from dict where word = %s",(word,))
        word_doc = cursor.fetchone()
        if word_doc:
            cursor.execute("update dict set definition = %s",(definition,))
        else:
            cursor.execute("insert into dict (word,definition) values (%s,%s)",(word,definition))
            cursor.execute("select * from dict where word = %s",(word,))
            word_doc = cursor.fetchone()

        columns = ('id','word','definition')
        results = dict(zip(columns,word_doc))
        self.write(results)
        cursor.close()
        self.application.db.commit()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()