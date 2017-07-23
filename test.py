import sqlalchemy

from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

print('Use sqlalchemy version is: sqlalchemy %s.' % sqlalchemy.__version__)

engine = create_engine('mysql+pymysql://root:root@localhost:3306/testdb?charset=utf8')
Base = declarative_base()

class  User(Base):
	__tablename__ = 'users'
	id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
	name = Column(String(20))
	fullname = Column(String(20))
	password = Column(String(20))
	def __repr__(self):
		  return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

##创建表
#Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

