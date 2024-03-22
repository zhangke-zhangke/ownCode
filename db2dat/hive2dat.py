# encoding=utf-8
import pymysql
import pandas as pd
import numpy as np
import datetime
from pyhive import hive



# 设置连接参数
host = '172.30.6.5' # Hive服务器地址
port = 10000 # Hive服务器端口号
username = 'hive' # Hive用户名
password = 'hive' # Hive密码
database = 'jxpoc_dm' # Hive数据库名
# auth = 'LDAP'
limit_date = 4



def get_data(sql):
    connection = hive.Connection(host=host, port=port, database=database)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
            col = [item[0] for item in cursor.description]
            result_data = pd.DataFrame(res, columns=col)
    #         result_data = result_data.apply(pd.to_numeric, errors='ignore')
    except Exception as e:
        print(e)
    finally:
        cursor.close()

    return result_data




# 将dat字段的df改为dat文件并写入
def dat_df_to_dat_file(df, dat_name):
    # final_ds_base_info.astype(str).to_csv(r'C:\Users\Lenovo\Desktop\aa.dat',sep='|@|')
    np.savetxt(fr'C:\Users\dell\Desktop\江西农信poc\测试数据\dat\{dat_name}.dat', df.values.astype('str'), delimiter='|@|', fmt='%s',encoding='utf-8', )
    # np.savetxt(fr'C:\Users\Lenovo\Desktop\{dat_name}.dat', df.values.astype('str'), delimiter='|@|', fmt='%s',encoding='utf-8', )



# 获取当前日期
def get_now_date():
    now_time = datetime.datetime.now()
    now_date = now_time.strftime('%Y-%m-%d')
    return now_date



def aml_sspcs_rpt():
    # 3号令
    sql = '''
        select *
        from psbc_js.aml_sspcs_rpt
    '''
    sspc_rpt = get_data(sql)
    dat_df_to_dat_file(sspc_rpt, f'P20210257_JS_FXQ_AML_SSPCS_RPT_{get_now_date().replace("-", "")}_0001')



def base_info():
    # 对私基本信息
    sql = '''
        select *
        from jxpoc_dm.zqy_idv_base_info
    '''
    idv_base_info = get_data(sql)
    dat_df_to_dat_file(idv_base_info, f'P20210257_JS_FXQ_IDV_BASE_IMG_{get_now_date().replace("-", "")}_0001')



    # 对公基本信息
    sql = '''
        select *
        from jxpoc_dm.zqy_corp_base_info
    '''
    corp_base_info = get_data(sql)
    dat_df_to_dat_file(corp_base_info, f'P20210257_JS_FXQ_CORP_BASE_IMG_{get_now_date().replace("-", "")}_0001')


def account_info():
    # 对公账户信息
    sql = '''
        select *
        from jxpoc_dm.zqy_corp_account_info
    '''
    corp_account_info = get_data(sql)
    dat_df_to_dat_file(corp_account_info, f'P20210257_JS_FXQ_CORP_OPN_ACCT_{get_now_date().replace("-", "")}_0001')



    # 对私账户信息
    sql = '''
        select *
        from jxpoc_dm.zqy_idv_account_info
    '''
    idv_account_info = get_data(sql)
    dat_df_to_dat_file(idv_account_info, f'P20210257_JS_FXQ_IDV_OPN_ACCT_{get_now_date().replace("-", "")}_0001')



def transflow():
    # 交易流水
    sql = '''
        select *
        from jxpoc_dm.zqy_transflow_info
    '''
    transflow_info = get_data(sql)
    dat_df_to_dat_file(transflow_info, f'P20210257_JS_FXQ_TRAN_{get_now_date().replace("-", "")}_' + str(0 + 1).zfill(4))


if __name__ == '__main__':


    base_info()

    account_info()

    transflow()

    # aml_sspcs_rpt()






