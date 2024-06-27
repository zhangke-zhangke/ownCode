import networkx as nx
from flask import current_app


# 根据度来评价社区
def centrality_community_with_degree(G):
    # nx.degree_centrality(G)   {0: 0.5, 2: 0.8333333333333333, 1: 0.16666666666666666, 4: 0.3333333333333333, 3: 0.16666666666666666, 10: 0.16666666666666666, 11: 0.16666666666666666}
    current_app.logger.info(f'基于度的社区中心性评价：\n{nx.degree_centrality(G)}')

    result = nx.degree_centrality(G)
    result_sorted = sorted(result.items(), key=lambda x: x[1], reverse=True)
    current_app.logger.info(f'基于度的社区中心性评价排序：\n{result_sorted}')


    return result_sorted




# 根据最短路径来评价社区
def centrality_community_with_shortest_path(G):
    # nx.betweenness_centrality(G,weight='weight')  {0: 0.0, 2: 0.16666666666666666, 1: 0.0, 4: 0.1, 3: 0.0, 10: 0.0, 11: 0.0}
    for key,value in nx.betweenness_centrality(G,weight='weight').items():
        pass






