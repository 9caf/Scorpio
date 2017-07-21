# 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class MinorPurchase(Base):
    # 表的名字:
    __tablename__ = 't_minor_purchase'

    # 表的结构:
    id = Column(int(8), primary_key=True)
    item = Column(String(255))
    remark = Column(String(255))
    operator = Column(String(20))
    create_time = Column(String(255))
    modify_time = Column(String(255))

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)