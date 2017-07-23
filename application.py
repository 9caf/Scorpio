# -*- coding: utf-8 -*-

__author__ = '106035405@qq.com'

from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import DBSession, pymysql

app = Flask(__name__)

#加载flask-sqlalchemy配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/testdb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.logger.debug(db)

class MinorPurchase(db.Model):
    # 表的名字:
    __tablename__ = 't_minor_purchase'

    # 表的结构:
    id = db.Column(db.Integer, db.Sequence('minorPurchase_id_seq'), primary_key=True)
    item = db.Column(db.String)
    remark = db.Column(db.String)
    operator = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    modify_time = db.Column(db.DateTime)

    def __init__(self, id, item, remark, operator, create_time, modify_time):
    	self.id = id
    	self.item = item
    	self.remark = remark
    	self.operator = operator
    	self.create_time = create_time
    	self.modify_time = modify_time

    def __repr__(self):
        return '<MinorPurchase %r>' % self.item

#自定义jinja2的日期格式化过滤器
def datetimeformat(value, format='%Y年%m月%d日'):
	return value.strftime(format)
app.jinja_env.filters['datetimeformat'] = datetimeformat

#登入第一个页面
@app.route('/index')
def index():
	__name__ = '登入查询第一个页面'
	try:
		page = request.args.get('page', 1, type = int)
		app.logger.debug(__name__ + '参数page = %d' % page)

		pagination = MinorPurchase.query.order_by(MinorPurchase.id.desc()).paginate(
			page, per_page=10, error_out=True
			)
		print(pagination.has_next)
		print(pagination.has_prev)
		print(pagination.iter_pages)
		print(pagination.next_num)

		query = pagination.items
		app.logger.info(__name__ + '>>> index()  查询成功！')
		return render_template('index.html', result = query, pagination = pagination)
	except TypeError as e:
		app.logger.error(__name__ + '运行类型错误  查询出错！')
		raise e
	except Exception as e:
		app.logger.error(__name__ + '>>> index()  查询出错！')
		raise e

#查询全部信息		
@app.route('/findall')
def findall():
	__name__ = '查询全部信息页面'
	try:
		query = MinorPurchase.query.order_by(MinorPurchase.id.desc()).all()
		app.logger.info(__name__ + '>>> findall()  查询成功！')
		return render_template('findall.html', result = query, num = len(query))
	except Exception as e:
		app.logger.error(__name__ + '>>> findall()  查询出错！')
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