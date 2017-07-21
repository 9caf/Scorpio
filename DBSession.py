# -*- coding: utf-8 -*-

# 导入:
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import pymysql

# 创建对象的基类:
Base = declarative_base()

# 定义MinorPurchase对象:
class MinorPurchase(Base):
    # 表的名字:
    __tablename__ = 't_minor_purchase'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    item = Column(String)
    remark = Column(String)
    operator = Column(String)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:root@localhost:3306/testdb?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

