#Louvain算法
import matplotlib.pyplot as plt
import networkx as nx
from community import community_louvain
import pandas as pd
import sys
from networkx.algorithms.community import louvain_communities
from networkx.algorithms.community import louvain_partitions
from networkx.algorithms.community import louvain
from common import plotGraph
import time
from flask import current_app



def runlouvain(G,resolution,threshold) -> dict:
    '''
    运行louvain算法
    :param G:          网络图
    :param resolution:  社区规模度，参数大于1则算法在社区计算时更倾向于筛选出更大的社区。参数默认值：1
    :param threshold:   模块化增益阈值，算法在计算合并社区时的模块化增益小于设置的阈值时，算法不再合并社区，此时算法结束。参数默认0.0000001
    :return:           社群划分json格式数据
    '''


    # community库下louvain版本，只支持非有向图
    # com = community_louvain.best_partition(G,weight='weight',resolution=0.5)
    # df_com = pd.DataFrame({'Group_id':com.values(),
    #                        'object_id':com.keys()})


    # networkx库下的louvain 直接返回社群
    com = louvain.louvain_communities(G,weight='weight',resolution=resolution,threshold=threshold)
    current_app.logger.info(f'louvain communities count: {len(com)}')

    # 社群划分结果
    com_result = {}
    com_info = {}
    for i in range(len(com)):
        # con_result[i+1] = G.subgraph(com[i]).nodes()
        # 社群编号从0开始   直接list(dict()) 省内存
        com_result[i] = list(com[i])
        com_info[i] = len(com[i])
        current_app.logger.info(f'community {i+1} count: {com_info[i]}')
        current_app.logger.info(f'community {i+1} nodes: {com_result[i]}')


    return com_result,com_info






r'''
    catgloy = []
    clue_list = []
    for i,th in enumerate(com):
        for clue in th:
            clue_list.append(clue)
            catgloy.append(i)
    # 团伙汇总dataframe
    df_com = pd.DataFrame({'Group_id':catgloy,
                           'object_id':clue_list}
                        )
    # 统计每个团伙人数 并降序
    df_com.groupby('Group_id').count().sort_values(by='object_id', ascending=False,inplace=True)
    # df_com.to_csv(r'C:\Users\dell\Desktop\python-graph\result\louvain_result_noweight.csv',index=False,encoding='utf-8')

    # # 调用画图函数画图
    # plotGraph(G,catgloy)



    return df_com
'''