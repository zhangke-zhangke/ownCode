# encoding=utf-8
from pyhive import hive
import pandas as pd
import sys
import datetime
from datetime import timedelta
from impala.dbapi import connect
import whisper



# 设置连接参数
host = '172.30.6.5' # Hive服务器地址
port = 10000 # Hive服务器端口号
username = 'hive' # Hive用户名
password = 'hive' # Hive密码
database = 'jxpoc_dm' # Hive数据库名
# auth = 'LDAP'
limit_date = 4



# 建立连接
conn = hive.Connection(host=host, port=port, database=database)
def get_sql_result(sql):
    # 执行查询并获取结果
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    columns = [desc[0].split('.')[-1] for desc in cursor.description]



    return results,columns

# 构造查询语句
query = 'select * from jxpoc_dm.et_base_ip_region_jspoc'
result,columns = get_sql_result(query)
# 将结果转换为DataFrame
partitions = pd.DataFrame(result, columns = columns)
print(partitions)


df_list = []
for i in range(partitions.shape[0]):
    # print(partitions['start_id'].iloc[i],partitions['end_id'].iloc[i])
    # list = []
    for c in range(partitions['start_id'].iloc[i],partitions['end_id'].iloc[i]+1):
        if partitions['province'].iloc[i] in ['香港','澳门']:
            df_list.append([c,partitions['province'].iloc[i]])
        else:
            df_list.append([c, partitions['country'].iloc[i]])
    # break

# print()

pd.DataFrame(df_list).to_csv('ip.csv',index=False,encoding='utf-8')


# start_dt = partitions['partition'].iloc[0].split('=')[-1]
# # print(start_dt) # 2021-01-01
# end_dt = partitions['partition'].iloc[-1].split('=')[-1]
# # print(end_dt)   # 2023-04-08
# all_partitions_list = []
# for i in range(partitions.shape[0]):
#     all_partitions_list.append(partitions['partition'].iloc[i].split('=')[-1])
#
#
# # sys.exit()
#
# final_list = []
# final_col = []
# for i,partition_dt in enumerate(all_partitions_list):
#     export_st_time = datetime.datetime.now()
#     print(f'执行导出第{i+1}个分区数据：{partition_dt}，当前时间：{export_st_time}')
#     every_day_sql = f'''
#         select *
#         from finance.fxq_tran
#         where dt = '{partition_dt}'
#     '''
#     result, columns = get_sql_result(every_day_sql)
#     if i == 0:
#         final_col.append(columns)
#     # 将结果添加到总列表中
#     # final_list.append(result)
#     final_list += result
#
#     export_ed_time = datetime.datetime.now()
#     print(f'{partition_dt}分区共查询{len(result)}条数据，结束时间：{export_ed_time}，当前分区耗时：{export_ed_time-export_st_time}')
#     # 测试 限制天数
#     if i == limit_date:
#         break
#
#
# df = pd.DataFrame(final_list,columns=columns)
# print(df)

