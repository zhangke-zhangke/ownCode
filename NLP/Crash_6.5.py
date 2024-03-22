import pymysql
import pandas as pd
import sys
import pymysql
from sqlalchemy import create_engine

connection = pymysql.connect(host='172.30.6.5', user='root', password='123456', database='financeData', port=int(3306))


try:
    with connection.cursor() as cursor:
        sql = '''
            SELECT `type`,`cust_no`,`in_44w`,`in_160w`,`suspicious`,CASE WHEN cust_no IN (SELECT DISTINCT 客户编号 FROM `JH_TRAN_ALL`) THEN 0 ELSE 1 END 'have_trade',`time`
            FROM `et_compare_result`
        '''
        cursor.execute(sql)
        res = cursor.fetchall()
        col = [item[0] for item in cursor.description]
        crash_result = pd.DataFrame(res,columns=col)
        print(crash_result)
        print(crash_result.info())

        engine = create_engine('mysql+pymysql://root:123456@172.30.6.5:3306/financeData?charset=utf8')
        crash_result.to_sql('python_et_compare_result', con=engine, if_exists='replace', index=False, )

finally:
    cursor.close()
















