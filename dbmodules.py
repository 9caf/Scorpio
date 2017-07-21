# -*- coding: utf-8 -*-

import pymysql

__author__ = '106035405@qq.com'

#MySQL数据库配置
host = 'localhost'
user = 'root'
passwd = 'root'
dbname = 'testdb'
charset = 'utf8mb4'

def queryall(sql, template):
	db = pymysql.connect(host = host, user = user, passwd = passwd, db = dbname, charset = charset)
	cursor = db.cursor()
	try:
		cursor.execute(sql)
		result = cursor.fetchall()
		db.commit()
		db.close()
		return result
	except Exception as e:
		raise e