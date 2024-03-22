import pymysql
import sys
import pymysql
from sqlalchemy import create_engine
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import sys
from sklearn.metrics import classification_report
from sklearn import tree
from sklearn.tree import _tree
from graphviz import Source
from ipywidgets import interactive
from IPython.display import SVG, display
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_graphviz
from sklearn import tree
import graphviz


def query_sql(cursor,sql):
    cursor.execute(sql)
    res = cursor.fetchall()
    col = [item[0] for item in cursor.description]
    crash_result = pd.DataFrame(res, columns=col)

    return crash_result




if __name__ == '__main__':
    connection = pymysql.connect(host='172.30.6.204', user='root', password='123456', database='datapipline',
                                 port=int(3306))
    cursor = connection.cursor()

    # 读取标签数据
    target_info = pd.read_excel(r'C:\Users\dell\Desktop\样本标签.xlsx')
    target_info = target_info[['卡号','是否可疑（人工）']]



    # 计算特征 —— 交易总金额
    sql = '''
            select `客户名称`,`查询账号`,`查询卡号`,sum(`交易金额`) `交易总金额`
            from `trade1`
            group by `客户名称`,`查询账号`,`查询卡号`
    '''
    df_sum_money = query_sql(cursor,sql)


    # 交易次数
    sql = '''
            select `客户名称`,`查询账号`,`查询卡号`,count(1) `交易笔数`
            from `trade1`
            group by `客户名称`,`查询账号`,`查询卡号`
    '''
    df_trade_count = query_sql(cursor,sql)


    # 入向交易笔数
    sql = '''
            select `客户名称`,`查询账号`,`查询卡号`,count(1) `入向交易笔数`
            from `trade1`
            where 借贷标志 = '进'
            group by `客户名称`,`查询账号`,`查询卡号`
    '''
    df_in_num = query_sql(cursor,sql)


    # 出向交易笔数
    sql = '''
            select `客户名称`,`查询账号`,`查询卡号`,count(1) `出向交易笔数`
            from `trade1`
            where 借贷标志 = '出'
            group by `客户名称`,`查询账号`,`查询卡号`
    '''
    df_out_num = query_sql(cursor,sql)


    # 交易总天数
    sql = '''
            select `客户名称`,`查询账号`,`查询卡号`,count(1) '交易总天数'
            from 
            (
                select `客户名称`,`查询账号`,`查询卡号`,substring(`交易时间`,1,10)
                from trade1
                group by `客户名称`,`查询账号`,`查询卡号`,substring(`交易时间`,1,10)
            ) a
            group by `客户名称`,`查询账号`,`查询卡号`                   
    '''
    df_sum_day = query_sql(cursor,sql)



    merge1 = pd.merge(df_sum_money,df_trade_count,on=['客户名称', '查询账号', '查询卡号'], how='inner')
    merge2 = pd.merge(merge1,df_in_num,on=['客户名称', '查询账号', '查询卡号'], how='inner')
    merge3 = pd.merge(merge2,df_out_num,on=['客户名称', '查询账号', '查询卡号'], how='inner')
    merge = pd.merge(merge3,df_sum_day,on=['客户名称', '查询账号', '查询卡号'], how='inner')




    final_result = pd.merge(target_info,merge,left_on=['卡号'],right_on=['查询卡号'],how='inner')
    final_result = final_result.iloc[:,1:]
    final_result['是否可疑（人工）'] = final_result['是否可疑（人工）'].apply(lambda x:1 if x == '可疑' else 0)
    print(final_result)
    print(final_result.info())


    x = final_result[['交易总金额','交易笔数','入向交易笔数','出向交易笔数','交易总天数']]
    y = final_result['是否可疑（人工）']
    print(x[['交易总金额','交易笔数']])


    # 两两组合新特征
    new_x = pd.DataFrame()
    new_x['交易总金额_交易笔数'] = x['交易总金额']+x['交易笔数']
    new_x['交易总金额_入向交易笔数'] = x['交易总金额']+x['入向交易笔数']
    new_x['交易总金额_出向交易笔数'] = x['交易总金额']+x['出向交易笔数']
    new_x['交易总金额_交易总天数'] = x['交易总金额']+x['交易总天数']
    new_x['交易笔数_入向交易笔数'] = x['交易笔数']+x['入向交易笔数']
    new_x['交易笔数_出向交易笔数'] = x['交易笔数']+x['出向交易笔数']
    new_x['交易笔数_交易总天数'] = x['交易笔数']+x['交易总天数']
    new_x['入向交易笔数_出向交易笔数'] = x['入向交易笔数']+x['出向交易笔数']
    new_x['入向交易笔数_交易总天数'] = x['入向交易笔数']+x['交易总天数']
    new_x['出向交易笔数_交易总天数'] = x['出向交易笔数']+x['交易总天数']
    print(new_x)




    # ds = GradientBoostingClassifier()
    # ds.fit(new_x,y)
    # print('对应特征项:',new_x.columns.tolist())
    # print("对私特征重要程度分别为：",ds.feature_importances_.tolist())



    Dtree = tree.DecisionTreeRegressor(max_depth=5,random_state=111)
    dtree = Dtree.fit(new_x, y)

    n_nodes = dtree.tree_.node_count
    children_left = dtree.tree_.children_left
    children_right = dtree.tree_.children_right
    feature = dtree.tree_.feature
    threshold = dtree.tree_.threshold


    print(n_nodes)
    print(children_left)
    print(children_right)
    print(feature)
    print(threshold)

    dot_data = tree.export_graphvizdot_data = tree.export_graphviz(dtree, out_file=None, )
    graph = graphviz.Source(dot_data)
    graph.render("dt")










