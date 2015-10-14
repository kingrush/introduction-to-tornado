#coding=utf-8
__author__ = 'knight'
import psycopg2
import psycopg2.extras

con = psycopg2.connect(host='localhost', port=5432, user='postgres', password='postgres', database='test')
cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("insert into dict(word,definition) values (%s,%s)",("perturb","Bother, unsettle, modify"))

con.commit()
cursor.close()
con.close()