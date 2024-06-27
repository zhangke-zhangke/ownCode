



import networkx as nx
import random
g = nx.karate_club_graph()  # 空手道俱乐部
for u ,v in g.edges:
    print(u ,v)
    g.add_edge(u, v, time=random.uniform(0, 1))  # 权值为(0,1)间的随机数
print(g.edges(data=True))
















