import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt



edges = pd.DataFrame(
    {
        "source": [0, 1, 4, 2, 2, 2, 10],
        "target": [2, 2, 3, 4, 0, 0, 11],
        "weight": [0.2, 1, 0.3, 0.1, 0.9, 0, 0.999]
    }
)
print(edges)
G = nx.from_pandas_edgelist(
    edges,
    edge_attr=["weight"],
    create_using=nx.MultiDiGraph(),
)
print(G)
print(G.edges(data=True))


# 社区中心度
# 分析数一个社区中每个节点中本社区的中心度
sub_graph = nx.subgraph(G,[0,2,3,4,5])
print(sub_graph)



print('================================')



# # 群聚系数
# # 这个在NetworkX里实现起来很简单，只需要调用方法nx.average_clustering(G) 就可以完成平均群聚系数的计算，而调用nx.clustering(G) 则可以计算各个节点的群聚系数。
# print(nx.average_clustering(G))

# 直径和平均距离
# nx.diameter(G)返回图G的直径（最长最短路径的长度），而nx.average_shortest_path_length(G)则返回图G所有节点间平均最短路径长度。
# print(nx.diameter(G,weight='weight'))
# print(nx.average_shortest_path_length(G,weight='weight'))


# # 匹配性
# # 调用 nx.degree_assortativity(G) 方法可以计算一个图的度匹配性。
# print(nx.degree_assortativity(G))


# 中心性

# 点度中心性
# 计算节点的度中心性。
print(nx.degree_centrality(G,))
# # 计算节点的入度中心性
# print(nx.in_degree_centrality(G))
# # 计算节点的出度中心性
# print(nx.out_degree_centrality(G))

# 紧密中心性
# 计算节点的接近中心性。
print(nx.closeness_centrality(G))

# 接近中心性
# 计算节点的中间性中心性。
print(nx.betweenness_centrality(G,weight='weight'))
# 计算边的中间性中心性
print(nx.edge_betweenness_centrality(G,weight='weight'))


# 画图
pos = nx.spring_layout(G)
nx.draw(G,pos,with_labels=True)
plt.show()


'''
Degree centrality measures.（点度中心性？）
degree_centrality(G)     Compute the degree centrality for nodes.
in_degree_centrality(G)     Compute the in-degree centrality for nodes.
out_degree_centrality(G)     Compute the out-degree centrality for nodes.

Closeness centrality measures.（紧密中心性？）
closeness_centrality(G[, v, weighted_edges])     Compute closeness centrality for nodes.

Betweenness centrality measures.（介数中心性？）
betweenness_centrality(G[, normalized, ...])     Compute betweenness centrality for nodes.
edge_betweenness_centrality(G[, normalized, ...])     Compute betweenness centrality for edges.

Current-flow closeness centrality measures.（流紧密中心性？）
current_flow_closeness_centrality(G[, ...])     Compute current-flow closeness centrality for nodes.
Current-Flow Betweenness

Current-flow betweenness centrality measures.（流介数中心性？）
current_flow_betweenness_centrality(G[, ...])     Compute current-flow betweenness centrality for nodes.
edge_current_flow_betweenness_centrality(G)     Compute current-flow betweenness centrality for edges.

Eigenvector centrality.（特征向量中心性？）
eigenvector_centrality(G[, max_iter, tol, ...])     Compute the eigenvector centrality for the graph G.
eigenvector_centrality_numpy(G)     Compute the eigenvector centrality for the graph G.

Load centrality.（彻底晕菜~~~）
load_centrality(G[, v, cutoff, normalized, ...])     Compute load centrality for nodes.
edge_load(G[, nodes, cutoff])     Compute edge load.

'''



