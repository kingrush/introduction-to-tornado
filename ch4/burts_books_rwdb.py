#coding=utf-8
__author__ = 'knight'
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import psycopg2
import psycopg2.extras
import os.path
from tornado.options import define,options

define("port",default=8000,help="run on the given port",type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler),
            (r"/recommended", RecommendedHandler),
            (r"/edit/([0-9Xx\-]+)", BookEditHandler),
            (r"/add", BookEditHandler)]
        settings = dict(template_path=os.path.join(os.path.dirname(__file__),"templates"),
                        static_path=os.path.join(os.path.dirname(__file__),"static"),
                        ui_modules={"Book":BookModule},
                        debug=True,)
        conn = psycopg2.connect(database="test",port="5432",user="postgres",host="localhost",password="postgres")
        self.conn = conn
        tornado.web.Application.__init__(self,handlers,**settings)

class BookEditHandler(tornado.web.RequestHandler):
    def get(self, isbn=None):
        book = dict()
        if isbn:
            cur = self.application.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("select * from book where isbn = %s",(isbn,))
            book = cur.fetchone();
        self.render("book_edit.html",page_title="zyy's book",header_text="Edit book",book=book)

    def post(self, isbn=None):
        import time
        import datetime
        book_fields = ['isbn','title','subtitle','image','author','date_released','description']
        cur = self.application.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        book = dict()
        if isbn:
            cur.execute("select * from book where isbn = %s",(isbn,))
            book = cur.fetchone();
        for key in book_fields:
            book[key] = self.get_argument(key,None)

        if isbn:
            cur.execute("update book set title = %s, subtitle = %s, image = %s, author = %s, date_released="
                        " %s, description = %s where isbn = %s",(book['title'],book['subtitle'],book['image'],book['author'],
                                                 book['date_released'],book['description'],isbn))
        else:
            book['date_released'] = datetime.date.today()
            cur.execute("insert into  book (isbn,title,subtitle,image,author,date_released,description) values (%s,%s,%s,%s,%s,%s,%s)",(book['isbn'],book['title'],
                                                                           book['subtitle'],book['image'],book['author'],
                                                 book['date_released'],book['description']))
        cur.close()
        self.application.conn.commit()

        self.redirect("/recommended")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",page_title="Yi yi's Books | Home",header_text="Welcome to Yi yi's Books!",)

class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        cur = self.application.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("select * from book")
        bks = cur.fetchall()
        columns = ('id','title','subtitle','image','author','date_added','date_released','isbn','description')
        results = []
        results = dict(zip(columns,bks))

        self.render("recommended.html",page_title="Burt's Books | Recommended Reading",header_text="Recommended Reading",
        books = bks)

class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string("modules/book.html",book=book,)
    def css_files(self):
        return "css\\recommended.css"
    def javascript_files(self):
        return "/static/js/recommended.js"


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()