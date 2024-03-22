import pymysql
import sys
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
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_graphviz,export_text
from sklearn import tree
import graphviz
from collections import deque
import re
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import numpy as np
import matplotlib.pyplot as plt
import flask


def connect_database(host,user,password,port,database):
    # connection = pymysql.connect(host='172.30.6.184', user='root', password='zqykj123', database='finance',port=int(3306))
    connection = pymysql.connect(host=host, user=user, password=password, database=database,port=int(port))
    cursor = connection.cursor()

    return cursor


def query_sql(cursor,sql):
    cursor.execute(sql)
    res = cursor.fetchall()
    col = [item[0] for item in cursor.description]
    crash_result = pd.DataFrame(res, columns=col)

    return crash_result


def reverse_df(crash_result):
    # 纵向表转横向
    new_df = crash_result.set_index(['card_no', 'index_name'])['index_value']
    new_df = new_df.unstack().rename_axis(columns=None).reset_index().fillna(0)

    return new_df


def get_data(cursor):
    # 获取特征及标签数据
    sql = '''
            select card_no,index_name,index_value
            from ai_index_vlist
            where create_time > date_add(now(),interval -3 month)
    '''
    original_df = query_sql(cursor,sql)
    # 列转行
    df = reverse_df(original_df)
    df = df.apply(pd.to_numeric, errors='ignore')

    # 所有的列名
    sql = '''
            select index_name
            from ai_index
    '''
    all_df = query_sql(cursor,sql)
    all_col = all_df['index_name'].tolist()
    all_col_df = pd.DataFrame(columns=all_col)

    final_df = pd.concat([all_col_df, df], sort=False)
    final_df.dropna(axis=1,inplace=True)
    final_df.fillna(0, inplace=True)


    return final_df




def tree_mode(x,y):
    Dtree = tree.DecisionTreeRegressor(max_depth=3,random_state=111)
    dtree = Dtree.fit(x, y)

    n_nodes = dtree.tree_.node_count
    children_left = dtree.tree_.children_left
    children_right = dtree.tree_.children_right
    feature = dtree.tree_.feature
    threshold = dtree.tree_.threshold

    return dtree


def tree_decide(x,dtree,final_result,white_all_count,black_all_count,recall_condition):
    # feature_names = x.columns
    # features = [feature_names[i] for i in range(len(feature_names))]
    # importances = clf.feature_importances_
    clf = dtree
    impurity = clf.tree_.impurity

    # global Conts
    global ContsNode
    global Path
    # Conts=[]#
    ContsNode = []
    Path = []
    global Results
    Results = []

    def print_decision_tree(tree, feature_names, offset_unit='' ''):
        left = tree.tree_.children_left
        right = tree.tree_.children_right
        threshold = tree.tree_.threshold
        value = tree.tree_.value

        if feature_names is None:
            features = [f'' % i for i in tree.tree_.feature]
        else:
            features = [feature_names[i] for i in tree.tree_.feature]

        def recurse(left, right, threshold, features, node, depth=0, ParentNode=0, IsElse=0):
            global Conts
            global ContsNode
            global Path
            global Results
            global LeftParents
            LeftParents = []
            global RightParents
            RightParents = []
            for i in range(len(left)):  # This is just to tell you how to create a list.
                LeftParents.append(-1)
                RightParents.append(-1)
                ContsNode.append("")
                Path.append("")

            for i in range(len(left)):  # i is node
                if (left[i] == -1 and right[i] == -1):
                    if LeftParents[i] >= 0:
                        if Path[LeftParents[i]] > " ":
                            Path[i] = Path[LeftParents[i]] + " AND " + ContsNode[LeftParents[i]]
                        else:
                            Path[i] = ContsNode[LeftParents[i]]
                    if RightParents[i] >= 0:
                        if Path[RightParents[i]] > " ":
                            Path[i] = Path[RightParents[i]] + " AND not " + ContsNode[RightParents[i]]
                        else:
                            Path[i] = " not " + ContsNode[RightParents[i]]
                    Results.append(" case when  " + Path[i] + "  then ''" + "{:4d}".format(i) + " " + "{:2.2f}".format(
                        impurity[i]) + " " + Path[i][0:180] + "''")

                else:
                    if LeftParents[i] >= 0:
                        if Path[LeftParents[i]] > " ":
                            Path[i] = Path[LeftParents[i]] + " AND " + ContsNode[LeftParents[i]]
                        else:
                            Path[i] = ContsNode[LeftParents[i]]
                    if RightParents[i] >= 0:
                        if Path[RightParents[i]] > " ":
                            Path[i] = Path[RightParents[i]] + " AND not " + ContsNode[RightParents[i]]
                        else:
                            Path[i] = " not " + ContsNode[RightParents[i]]
                    if (left[i] != -1):
                        LeftParents[left[i]] = i
                    if (right[i] != -1):
                        RightParents[right[i]] = i
                    ContsNode[i] = "( " + features[i] + " <= " + str(threshold[i]) + " ) "
        recurse(left, right, threshold, features, 0, 0, 0, 0)
    print_decision_tree(dtree, x.columns)
    SqlOut = ""
    for i in range(len(Results)):
        SqlOut = SqlOut + Results[i] + " end," + chr(13) + chr(10)

    # 将规则组合及规则指标组合成dataframe
    rule_info = []
    for i in SqlOut.strip().split("' end,")[:-1]:
        # 规则特征
        rule_feature = i.split('then')[0].replace('case when', '').replace('(', '').replace(')', '')
        every_feature = rule_feature.split('AND')
        # 规则逻辑特征拼接
        final_feature = ''
        for c, every in enumerate(every_feature):
            if 'not' in every:
                new_f = every.replace('not  ', '').replace('<=', '>')
                final_feature += new_f
            else:
                final_feature += every
            # & 逻辑拼接，方便后续筛选
            if c != len(every_feature) - 1:
                final_feature += '&'
        print("当前规则组合：",final_feature.strip())

        if len(set(final_result.query(final_feature)['TARGET_LABEL'].tolist())) == 1:
            print('当前规则推荐计算结果，无标签为0或为1的数据！\n')
        else:
            current_rule_target_info = dict(final_result.query(final_feature)['TARGET_LABEL'].value_counts())
            current_white_count = current_rule_target_info.get(0)
            current_black_count = current_rule_target_info.get(1)
            # 召回精准指标计算
            recall = current_black_count / black_all_count
            precision = current_black_count / (current_white_count + current_black_count)
            print(f"当前规则指标，召回：{recall},精准：{precision}")
            # 判断新规则的召回率是否高于接口传入的自定义的召回率
            if recall <= recall_condition:
                print('当前规则召回率低于自定义召回率阈值，舍弃不用！\n')
                continue
            # 满足阈值后再添加
            print('\n')
            rule_info.append([final_feature.strip(),recall,precision])

    # 规则组合df
    rule_detail_df = pd.DataFrame(rule_info,columns=['规则组合详情','召回率','精准率'])
    # 以召回降序排序
    rule_detail_df.sort_values(by=['召回率'],ascending=False,inplace=True)
    print(rule_detail_df)

    return_rule_detail = []
    return_num = 0
    if rule_detail_df.shape[0] >= 3:
        return_num = 3
    else:
        return_num = rule_detail_df.shape[0]
    for i in range(return_num):
        rule = rule_detail_df['规则组合详情'].iloc[i]
        rule_recall = rule_detail_df['召回率'].iloc[i]
        rule_precision = rule_detail_df['精准率'].iloc[i]

        rule_detail = []
        rule_feature_list = rule.strip().split('&')
        for i in range(len(rule_feature_list)):
            feature_args_parser = rule_feature_list[i].strip().split(' ')
            b = {}
            b['index_name'] = feature_args_parser[0]
            b['index_value'] = feature_args_parser[2]
            b['index_operation'] = feature_args_parser[1]
            rule_detail.append(b)

        # 规则指标
        new_rule = {}
        new_rule['index'] = rule_detail
        new_rule['RECALL'] = rule_recall
        new_rule['PRECISION'] = rule_precision
        return_rule_detail.append(new_rule)


    return return_rule_detail





'''
    接口入口
'''
server = flask.Flask(__name__)
@server.route('/newRule', methods=['get', 'post'])
def run():
    # 接收API参数
    host = flask.request.values.get('host')
    user = flask.request.values.get('user')
    password = flask.request.values.get('password')
    port = flask.request.values.get('port')
    database = flask.request.values.get('database')
    recall_condition = float(flask.request.values.get('recallCondition'))

    # 连接database
    cursor = connect_database(host,user,password,port,database)
    final_result = get_data(cursor)
    # 获取标签情况
    target_info = dict(final_result['TARGET_LABEL'].value_counts())
    white_all_count = target_info.get(0)
    black_all_count = target_info.get(1)

    y = final_result['TARGET_LABEL']
    x_col = [i for i in final_result.columns if i not in ['TARGET_LABEL','card_no']]
    x = final_result[x_col]
    # 树模型
    dtree = tree_mode(x,y)

    # 解析并组合
    return_rule_info = tree_decide(x,dtree,final_result,white_all_count,black_all_count,recall_condition)


    return flask.jsonify(return_rule_info)




if __name__ == '__main__':
    server.run(debug=True,port='8888',host='0.0.0.0')

    # run()
    # http://172.30.4.81:8888/newRule?host=172.30.6.184&user=root&password=zqykj123&database=finance&port=3306&recallCondition=0.3


    # http://172.30.4.81:8888/newRule?host=172.30.6.184&user=root&password=zqykj123&database=finance&port=3306