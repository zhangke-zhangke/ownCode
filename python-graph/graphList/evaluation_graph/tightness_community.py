import networkx as nx





# 该函数计算图中每个社区的紧密度。
# 社团的紧密度是社团中所有节点对之间的最短路径长度之和。
def tightness_community_with_graph(G):

    # {0: 0.2222222222222222, 2: 0.3333333333333333, 1: 0.0, 4: 0.3, 3: 0.2962962962962963, 10: 0.0, 11: 0.16666666666666666}
    nx.closeness_centrality(G)

