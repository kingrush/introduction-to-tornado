#coding=utf-8
__author__ = 'knight'
import psycopg2

try:
    conn = psycopg2.connect(database="test",port="5432",user="postgres",host="localhost",password="postgres")
    cur = conn.cursor()
    cur.execute('select * from dict;')
    rows = cur.fetchall()
    print( "查询数据库结果:",rows)
except:
    print("操作异常")