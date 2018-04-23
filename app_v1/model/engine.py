# 数据库model --2018-4-21
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index,DateTime
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime, sys

from ..config.config import Conf

#连接数据库(需要安装sqlalchemy和pymysql)
engine = create_engine(Conf.MYSQL_INFO) 

Base 	   = declarative_base() #创建一个基类

# alembic 模块是用于数据库迁移的一个模块,它可以增加列,删除列等等,但不能改变已有列的特性,比如String(100)
# alembic revision --autogenerate -m 'add column head_picture'生成一个py文件,用于数据版本更新
# alembic upgrade 版本号 更新到某个版本
# alembic upgrade head  更新到最新的版本
# alembic downgrade head 回退到最初的版本
# alembic downgrade 版本号 回退到某个版本



'''Session的主要目的是建立与数据库的会话，它维护你加载和关联的
   所有数据库对象。它是数据库查询（Query）的一个入口'''
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))

class User(Base):

	__tablename__ = "user"

	id 		     	= Column('id'				, Integer		, primary_key=True			)
	phone_number 	= Column('phone_number'		, String(11)	, index=True				)
	password     	= Column('password'			, String(30)								)
	nickname     	= Column('nickname'	 		, String(30)	, index=True, nullable=True	)
	head_picture    = Column('head_picture'		, String(100)   , index=True, default=''  	)
	alias           = Column('alias'            , String(10)    , default=''				)
	register_time	= Column('register_time'	, DateTime		, index=True, default=datetime.datetime.now	)

def init_db():
	Base.metadata.create_all(engine)

init_db()