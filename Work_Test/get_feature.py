import pymysql
import pandas as pd
import sys
import pymysql
from sqlalchemy import create_engine

connection = pymysql.connect(host='172.30.6.204', user='root', password='123456', database='zqyccserver_JR', port=int(3306))


try:
    with connection.cursor() as cursor:
        sql = '''
            select a.card_no,a.target_value,b.target_description
            from
            (
                select card_no,target_type,target_value
                from et_target_info
                where case_id  = '5d009343_5ab3_4a0d_9c2b_e1c31266c1d5'
            ) a
            inner join
            (
                select target_type,target_description
                from rs_target
            ) b
            on a.target_type = b.target_type    
        '''
        cursor.execute(sql)
        res = cursor.fetchall()
        col = [item[0] for item in cursor.description]
        crash_result = pd.DataFrame(res,columns=col)
        print(crash_result)

        new_df = crash_result.set_index(['card_no','target_description'])['target_value']
        new_df = new_df.unstack().rename_axis(columns=None).reset_index().fillna(0)
        print(new_df)
        print(new_df.info())

finally:
    cursor.close()










































