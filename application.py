# -*- coding: utf-8 -*-

__author__ = '106035405@qq.com'

from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql

#加载flask框架
app = Flask(__name__)

#加载flask-sqlalchemy配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/testdb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.logger.debug(db)

#定义零星采购的信息属性Model
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
		pagination = MinorPurchase.query.order_by(MinorPurchase.id.desc()).paginate(
			page, per_page=10, error_out=True
			)
		query = pagination.items
		app.logger.info(__name__ + '>>> index()  查询成功！')
		return render_template('index.html', result = query, pagination = pagination)
	except Exception as e:
		app.logger.error(__name__ + '数据库操作错误')
		raise e

#查询当前采购信息详情
@app.route('/query/<int:id>')
def query(id):
	__name__ = '查询当前采购信息详情'
	try:
		query = MinorPurchase.query.filter_by(id = id).first_or_404()
		app.logger.info(__name__ + '>>> query_here()  查询成功！')
		return render_template('query.html', result = query)
	except Exception as e:
		app.logger.error(__name__ + '数据库操作错误')
		raise e

#新增信息
@app.route('/new', methods=['GET', 'POST'])
def new():
	__name__ = '新增采购信息页面'
	if request.method == 'POST':
		app.logger.debug(__name__ + 'hello, here.')
		item = request.form['item']
		remark = request.form['remark']
		operator = request.form['operator']
		obj = MinorPurchase(None, item, remark, operator, None, None)
		try:
			db.session.add(obj)
			db.session.commit()
			app.logger.info(__name__ + '>>> new()  新增采购信息成功！')
			query = MinorPurchase.query.filter_by(operator = operator).order_by(MinorPurchase.id.desc()).first()
			app.logger.info(__name__ + '>>> query_here()  查询新增信息成功！返回编号')
			return render_template('query.html', result = query)
		except Exception as e:
			app.logger.error(__name__ + '数据库操作错误')
			raise e
	else:
		return render_template('new.html')

#编辑信息
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
	__name__ = '编辑采购信息页面'
	app.logger.debug(__name__ + '看看id等于多少：' + str(id))
	if request.method == 'POST':
		app.logger.debug(__name__ + 'hello, here.')
		obj = MinorPurchase.query.filter_by(id = id).first_or_404()
		obj.id = request.form['pk_id']
		obj.item = request.form['item']
		obj.remark = request.form['remark']
		obj.operator = request.form['operator']
		obj.create_time = request.form['create_time']
		try:
			db.session.add(obj)
			db.session.commit()
			app.logger.info(__name__ + '>>> edit()  修改采购信息成功！')
			query = MinorPurchase.query.filter_by(id = id).first_or_404()
			app.logger.info(__name__ + '>>> query_here()  查询新增信息成功！返回采购信息')
			return render_template('query.html', result = query)
		except Exception as e:
			app.logger.error(__name__ + '数据库操作错误')
			raise e
	else:
		app.logger.debug(__name__ + '跑到这里来了')
		query = MinorPurchase.query.filter_by(id = id).first_or_404()
		app.logger.info(__name__ + '>>> query_here()  查询成功！')
		return render_template('edit.html', result = query)

#删除信息
@app.route('/delete/<int:id>')
def delete(id):
	__name__ = '删除采购信息页面'
	obj = MinorPurchase.query.filter_by(id = id).first_or_404()
	try:
		db.session.delete(obj)
		db.session.commit()
		app.logger.info(__name__ + '>>> delete()  删除采购信息成功！')
		return index()
	except Exception as e:
		app.logger.error(__name__ + '数据库操作错误')
		raise e

#按条件查询页面
@app.route('/query_mode')
def queryMode():
	__name__ = '按条件查询页面'
	app.logger.info(__name__ + '现在走到这里了。')
	return render_template('query_mode.html')

#按条件查询信息
@app.route('/search')
def queryByElement():
	__name__ = '个别查询采购信息页面'
	app.logger.debug(__name__ + 'hello, here.')
	item = request.args.get('item', '')
	words = '%' + item + '%'
	app.logger.debug(__name__ + 'words = ' + words)

	page = request.args.get('page', 1, type = int)
	pagination = MinorPurchase.query.filter(MinorPurchase.item.like(words)).order_by(MinorPurchase.id.desc()).paginate(
		page, per_page=10, error_out=True
	)
	query = pagination.items
	if query:
		app.logger.info(__name__ + '>>> queryByElement()  查询成功！')
		return render_template('index_result.html', result = query, pagination = pagination, item_p = '&item=' + item)
	else:
		return render_template('error.html'), 404

#错误404页面
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0')