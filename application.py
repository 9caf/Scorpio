# -*- coding: utf-8 -*-

__author__ = '106035405@qq.com'

from flask import Flask, render_template, request, url_for
app = Flask(__name__)

import pymysql

db = pymysql.connect(host="localhost", user="root", passwd="root", db="testdb", charset="utf8mb4")
cursor = db.cursor()
cursor.execute("SELECT * FROM t_lingxing")
data = cursor.fetchall()

@app.route('/')
def index():
	for row in data:
		id = row[0]
		pjname = row[1]
		pjmark = row[2]
		print('id : %s ' % id + ', 项目: %s ' % pjname + ', 说明： %s' % pjmark )
	return 'OK'

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

if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0')