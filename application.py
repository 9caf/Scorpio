# -*- coding: utf-8 -*-

__author__ = '106035405@qq.com'

from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON, as_json
import pymysql, json

#加载flask框架
app = Flask(__name__)

#加载flask-sqlalchemy配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/testdb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.logger.debug(db)

#加载flask-json配置
FlaskJSON(app)
app.config['JSON_ADD_STATUS'] = False
app.config['JSON_DATETIME_FORMAT'] = '%Y年%m月%d日'

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

    def to_dict(self):
    	return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

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
	except TypeError as e:
		app.logger.error(__name__ + '运行类型错误  查询出错！')
		raise e
	except Exception as e:
		app.logger.error(__name__ + '>>> index()  查询出错！')
		raise e

@app.route('/dengji', methods=['GET', 'POST'])
def dengji():
	if request.method == 'POST':
		return redirect(url_for('details'))
	else:
		return render_template('dengji.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

#查询当前采购信息详情
@app.route('/query/<int:id>', methods=['GET', 'POST'])
@as_json
def query_here(id):
	__name__ = '查询当前采购信息详情'
	if request.method == 'POST':
		pass
	else:
		try:
			query = MinorPurchase.query.filter_by(id = id).first_or_404()
			app.logger.info(__name__ + '>>> query_here()  查询成功！')
			return query.to_dict()
		except Exception as e:
			app.logger.error(__name__ + '>>> query_here()  查询出错！')
			raise e

if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0')