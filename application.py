# -*- coding: utf-8 -*-

__author__ = '106035405@qq.com'

from flask import Flask, render_template, request, url_for
import datetime, DBSession

app = Flask(__name__)

def datetimeformat(value, format='%Y年%m月%d日'):
	return value.strftime(format)

app.jinja_env.filters['datetimeformat'] = datetimeformat

##暂时保留‘/’根目录路由，日后改为用户登陆
# @app.route('/')
# def function0():
# #	for row in result:
# #		id = row[0]
# #		pjname = row[1]
# #		pjmark = row[2]
# #		print('id : %s ' % id + ', 项目: %s ' % pjname + ', 说明： %s' % pjmark )
# 	db = pymysql.connect(host="localhost", user="root", passwd="root", db="testdb", charset="utf8mb4")
# 	cursor = db.cursor()
# 	cursor.execute("INSERT INTO t_lingxing(pjname, pjmark) VALUES ('手机', '徐超')")
# 	#result = cursor.fetchall()
# 	db.commit()
# 	db.close()

# 	print('Do insert()')
# 	return 'OK'

##已成功查询最新10条数据
# @app.route('/index')
# def function1():
# 	db = pymysql.connect(host="localhost", user="root", passwd="root", db="testdb", charset="utf8mb4")
# 	cursor = db.cursor()
# 	try:
# 		sql = 'SELECT * FROM `t_minor_purchase` ORDER BY id DESC LIMIT 10'
# 		cursor.execute(sql)
# 		result = cursor.fetchall()
# 		db.commit()
# 		db.close()
# 	except Exception as e:
# 		app.logger.error('捕捉异常，查询出错！')
# 		raise
# 	finally:
# 		app.logger.info('查询成功：' + sql)
# 	return render_template('index.html', result = result)

# #已成功使用pymysql制作的modules操作数据库
# @app.route('/index')
# def index():
# 	try:
# 		sql = 'SELECT * FROM `t_minor_purchase` ORDER BY id DESC LIMIT %d' % page + ', %d' % ()
# 		template = 'index.html'
# 		result = dbmodules.queryall(sql, template)
# 		app.logger.info('查询成功！SQL: %s，' % sql + 'template: %s' % template)
# 		return render_template(template, result = result)
# 	except Exception as e:
# 		app.logger.error('查询出错！SQL: %s，' % sql + 'template: %s' % template)
# 		raise e

@app.route('/index')
def index():
	try:
		session = DBSession.DBSession()
		query = session.query(DBSession.MinorPurchase).order_by(DBSession.MinorPurchase.id.desc()).limit(10).all()
		app.logger.info('>>> session.query(DBSession.MinorPurchase).order_by(DBSession.MinorPurchase.id.desc()).limit(10).all()  查询成功！')
		# 关闭Session:
		session.close()
		return render_template('index.html', result = query)
	except Exception as e:
		app.logger.error('>>> session.query(DBSession.MinorPurchase).order_by(DBSession.MinorPurchase.id.desc()).limit(10).all()  查询出错！')
		raise e

#查询全部信息		
@app.route('/findall')
def findall():
	try:
		session = DBSession.DBSession()
		query = session.query(DBSession.MinorPurchase).all()
		app.logger.info('>>> session.query(DBSession.MinorPurchase).all()  查询成功！')
		# 关闭Session:
		session.close()
		return render_template('findall.html', result = query, num = len(query))
	except Exception as e:
		app.logger.error('>>> session.query(DBSession.MinorPurchase).all()  查询出错！')
		raise e

@app.route('/dengji', methods=['GET', 'POST'])
def dengji():
	if request.method == 'POST':
		return redirect(url_for('details'))
	else:
		return render_template('dengji.html')

@app.route('/details')
def details():
	return render_template('details.html')
	
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)

if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0')