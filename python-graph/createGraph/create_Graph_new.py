import networkx as nx
from sqlalchemy import and_,or_,text
from createGraph import orm_session as orm
from createGraph import hive_data
import pandas as pd
from flask import request,Blueprint,jsonify,redirect,url_for,current_app
from flask import after_this_request
from common.cal_weight import graphWeightCal
import json
from common.connect_database import conDatabase



# 蓝图
creat_graph = Blueprint('creat_graph',__name__)
'''
    to do : create nx.graph
    step:
        1、ds托管sql创建图算法所需数据  zqy_transflow_info_python
        2、ds托管sql计算边权重  zqy_transflow_info_python_weight
        -------------python----------------------------------
        3、图算法被调时，直接取带权重的数据并入图
'''




@creat_graph.route('/creatNxGraph',methods=['get','post'])
def creat_nx_graph() -> nx.MultiDiGraph:
    '''
    :return: graph object
    '''
    # 验证数据库引擎
    if not conDatabase.available_con('hive'):
        raise ValueError('暂不支持该数据库！')

    # 初始化并连接数据库
    sqldatabase = conDatabase.initSqlObject('hive')
    exesql = '''
        select 
            card_no 
	        ,cnter_card_no
	        ,0.1 as weight
        from bojs_dm.zqy_transflow_info
        limit 1000
    '''
    df = sqldatabase.querySql(exesql)
    print(df.head(5))

    a = nx.MultiDiGraph()


    # dataframe to graph         nx.MultiDiGraph
    G = nx.from_pandas_edgelist(df, source='card_no', target='cnter_card_no', edge_attr='weight', create_using=nx.MultiDiGraph())
    current_app.logger.info(f'入图成功，图对象信息：{G}')



    # 过滤度小于2的点，减小数据量
    # remove = [node for node, degree in dict(G.degree()).items() if degree < 5]
    # G.remove_nodes_from(remove)
    # print(G)


    # 设置边属性
    node_attributes = {}
    for node,attributes in df.iterrows():
        df_dict = dict(attributes)
        node_attributes[df_dict.get('查询卡号')] = {key:df_dict.get(key) for key in ['客户名称']}
        node_attributes[df_dict.get('交易对方卡号')] = {key:df_dict.get(key) for key in ['交易对方名称']}
    nx.set_node_attributes(G,node_attributes)
    current_app.logger.info('create_nx_graph执行完成')



    return G



# creat_nx_graph()