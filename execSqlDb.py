
import sys


class T:
    _instance = None

    # __new__返回的就是后续函数（包括__init__）的第一个self参数
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print('初始化')


t1 = T()
t2 = T()


sys.exit()


import sys

'''
python中查询数据库（mysql、hive、pg等等）皆有两种方法。
第一种通过orm工具查询，但需要定义好数据模型。
第二章编写原生sql语句，通过建立的数据库engine执行语句。
'''

# 直接sql执行
import pymysql
import pandas as pd

import pymysql


class MySQLManager:
    # 确保单例模式
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='test',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

    def query(self, sql, args=None):
        self.cursor.execute(sql, args or ())
        return self.cursor.fetchall()

    def execute(self, sql, args=None):
        self.cursor.execute(sql, args or ())
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


# 1、编写sql语句
sql = '''
    select * from user
'''
# 使用示例
db = MySQLManager()
db.query("SELECT * FROM users")
db.execute("UPDATE users SET name=%s WHERE id=%s", ("张三", 1))


sys.exit()

# orm执行
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据模型需继承Base
Base = declarative_base()

class User(Base):
    # 表名
    __tablename__ = 'user'

    # 表字段
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# 创建数据库连接引擎
engine = create_engine(
    # 数据库连接字符串/jdbc
    'sqlite:///example.db',
    # 是否开启日志打印
    echo=False
)
# 创建表
Base.metadata.create_all(engine)

# 创建数据库连接会话
DbSession = sessionmaker(bind=engine)
dbSession = DbSession()

# 新增
addUser = User()
addUser.id = 1
addUser.name = 'lisi'
addUser.age = 25
dbSession.add(addUser)
dbSession.commit()
# 查询
user_all = dbSession.query(User).all()
for u in user_all:
    print(u.__dict__)
# 修改
mUser = dbSession.query(User).filter(User.id == 1).first()
if mUser:
    mUser.name = 'zhangke'
    dbSession.commit()
# 删除
mUser = dbSession.query(User).filter(User.id == 1).first()
if mUser:
    dbSession.delete(mUser)
    dbSession.commit()
