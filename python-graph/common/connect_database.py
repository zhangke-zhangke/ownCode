import pandas
from flask import current_app
from common.conf import *
import pymysql
import pandas as pd
from pyhive import hive






class conDatabase():

    def __init__(self,connection) -> None:
        '''
        :param connection: sql.connection object
        '''
        # self.conn = hive.Connection(host=hive_host, port=hive_port, database=hive_database)
        self.conn = connection
        self.support_database = []

    @staticmethod
    def get_support_database() -> list:
        support_database = []
        support_database.append('hive')
        support_database.append('mysql')

        return support_database

    @staticmethod
    def available_con(database) -> bool:
        '''
        :param database: 数据库引擎
        :return:
        '''
        if database in conDatabase.get_support_database():
            return True
        return False

    @classmethod
    def initSqlObject(cls,sqlMethod) -> object:
        '''
        :param sqlMethod:
        :return: new class
        '''
        if sqlMethod == 'hive':
            connection = hive.Connection(host=hive_host, port=hive_port, database=hive_database)
        elif sqlMethod == 'mysql':
            connection = pymysql.connect(host=host, user=user, password=password, database=database, port=int(port))
        else:
            raise ValueError('选择需要连接的数据库，列如：mysql 或 hive')
        # 根据连接重构类
        sqlObject = cls(connection)
        current_app.logger.info(f'----------初始化{sqlMethod}数据库连接！')

        return sqlObject

    # 执行sql语句
    def executeSql(self,ddl_sql) -> None:
        '''
        :param ddl_sql:
        :return: None
        '''
        with self.conn.cursor() as cursor:
            cursor.execute(ddl_sql)

    # 查询sql语句
    def querySql(self,query_sql) -> pandas.DataFrame:
        '''
        :param query_sql:
        :return: sql result on dataframe
        '''
        with self.conn.cursor() as cursor:
            cursor.execute(query_sql)

            results = cursor.fetchall()
            columns = [desc[0].split('.')[-1] for desc in cursor.description]
            # 封装dataframe
            hive_sql_df = pd.DataFrame(results, columns=columns)

        return hive_sql_df

