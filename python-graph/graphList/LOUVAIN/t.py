#导入建网络模型包，导入科学绘图包
import networkx as nx
import matplotlib.pyplot as plt
'''
随机生成网络 用erdos_renyi_graph(n,p)方法生成一个含有n个节点、
以概率p连接的ER随机图，在本程序中以概率0.8连接20个节点中的每一对节点，完成图形。
'''

for i in range(1,11):
    rate = i/10
    print(rate)
    G  = nx.erdos_renyi_graph(20,rate)
    nx.draw(G,
            with_labels=True,
            pos=nx.kamada_kawai_layout(G),
            #width=edgewidth,
            node_size=500,
            alpha=0.8,
            node_color="r",
            edge_color="DeepPink"
            )
    text = 'P={rate} Networks Wu'.format(rate=rate)
    plt.title(text, fontsize = 20)
    plt.show()