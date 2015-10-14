#coding=utf-8
__author__ = 'knight'
import psycopg2
import psycopg2.extras


conn = psycopg2.connect(database="test",port="5432",user="postgres",host="localhost",password="postgres")
cur = conn.cursor()
cur.execute('select * from dict;')
cur.execute("insert into book (title,subtitle,image,author,date_added,date_released,isbn,description) values"
            "(%s,%s,%s,%s,%s,%s,%s,%s)",('RESTful Web Services','Web services for the real world',
             '/static/images/restful_web_services.gif','Toby Segaran','1997-09-01','2007-07-01',
             '978-0-596-52932-1','<p>[...]</p>'))
cur.close()
conn.commit()