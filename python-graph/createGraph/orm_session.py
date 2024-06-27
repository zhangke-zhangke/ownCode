# models.py
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from common.conf import *
# from createGraph.hive_data import engine as hive_engine
# from createGraph.mysql_data import engine as mysql_engine




# 创建引擎
# 当且仅当使用LDAP或CUSTOM模式时需要设置密码;删除密码或使用其中一种模式
engine = create_engine(
    # f"hive+pyhive://<hive_username>:<hive_password>@<hive_host>:<hive_port>/<hive_database>?auth=<hive_auth>",
    f"hive://{hive_username}:{hive_password}@{hive_host}:{hive_port}/{hive_database}?auth={hive_auth}",
    # "mysql+pymysql://tom@127.0.0.1:3306/db1?charset=utf8mb4", # 无密码时
    # 超过链接池大小外最多创建的链接
    max_overflow=0,
    # 链接池大小
    pool_size=5,
    # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
    pool_timeout=10,
    # 多久之后对链接池中的链接进行一次回收
    pool_recycle=1,
    # 查看原生语句（未格式化）
    echo=True,
    # ping dbapi before every query
    pool_pre_ping = True
)



# 绑定引擎
Session = sessionmaker(bind=engine)
# 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
# 内部会采用threading.local进行隔离
session = scoped_session(Session)



