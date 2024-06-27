import networkx as nx
import matplotlib.pyplot as plt
from common.conf import *




plt.rcParams['font.sans-serif'] = ['SimHei']  # 在图中正确显示中文
plt.rcParams['axes.unicode_minus'] = False  # 默认是使用Unicode负号，设置正常显示字符，如正常显示负号




def plotGraph(G,catgloy):
    plt.figure(figsize=(60, 10))

    # draw  spring_layout
    pos = nx.spring_layout(G)
    # 显示
    nx.draw(G,pos,with_labels=True)
    # nx.draw(G,pos, with_labels=True, connectionstyle='arc3,rad=0.1')

    # node label
    node_lables = {}
    for node in G.nodes:
        node_lables[node] = node

    # 颜色设置
    colors = ['DeepPink', 'orange', 'DarkCyan', '#A0CBE2', '#3CB371', 'b', 'orange', 'y', 'c', '#838B8B', 'purple',
              'olive', '#A0CBE2', '#4EEE94'] * 500
    colors = [colors[i] for i in catgloy]
    # 画点label
    nx.draw_networkx_nodes(G,pos,node_size=200,node_color=colors)
    # nx.draw_networkx_labels(G,pos,labels=node_lables)


    # edge label
    edge_labels = {}

    # 单向边
    # edge_labels = dict([([u, v,], d['交易金额'])
    #                     for u, v, d in G.edges(data=True)])

    # 多项边
    for u, v, d in G.edges(data=True):
        edge_labels[(u,v)] = d

    # 画变label
    nx.draw_networkx_edges(G,pos,edge_color=colors)
    nx.draw_networkx_edge_labels(G,pos,font_size=5)
    # nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_size=5)


    # 保存截图
    plt.savefig("Graph.png", format="PNG")
    plt.axis('off')
    plt.show()
