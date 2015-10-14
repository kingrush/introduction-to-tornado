#coding=utf-8
__author__ = 'knight'
import psycopg2

try:
    conn = psycopg2.connect(database="test",port="5432",user="postgres",host="localhost",password="postgres")
    cur = conn.cursor()
    cur.execute('insert into dict(key,definition) values(%s,%s)',('perturb',"Bother, unsettle,modify"))

    conn.commit()
except:
    print("操作异常")