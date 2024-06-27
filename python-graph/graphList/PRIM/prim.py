from graphList.PRIM.pq import PriorityQueue, Graph, Vertex
# 最小生成树prim算法
# G - 无向赋权图
# start - 开始节点
# 返回从开始节点创建最小生成树
def prim(G, start):
    pq = PriorityQueue()  # 创建优先队列
    start.setDistance(0)  # 起点最小权重代价设置为0，其它节点最小权重代价默认maxsize
    # 将节点排入优先队列，start在最前面
    pq.buildHeap([(v.getDistance(), v) for v in G])
    while not pq.isEmpty():
        # 取距离*已有树*最小权重代价的节点出队列，作为当前节点
        # 当前节点已解出最小生成树的前驱pred和对应最小权重代价dist
        currentVert = pq.delMin()
        # 遍历节点的所有邻接节点
        for nextVert in currentVert.getConnections():
            # 从当前节点出发，逐个检验到邻接节点的权重
            newCost = currentVert.getWeight(nextVert)
            # 如果邻接节点是"安全边"，并且小于邻接节点原有最小权重代价dist，就更新邻接节点
            if nextVert in pq and newCost < nextVert.getDistance():
                # 更新最小权重代价dist
                nextVert.setPred(currentVert)
                # 更新返回路径
                nextVert.setDistance(newCost)
                # 更新优先队列
                pq.decreaseKey(nextVert, newCost)






G = Graph()
ndedge = [('A', 'B', 2), ('A', 'C', 3), ('B', 'C', 1),
          ('B', 'D', 1), ('B', 'E', 4), ('C', 'F', 5),
          ('D', 'E', 1), ('E', 'F', 1), ('F', 'G', 1)]
for nd in ndedge:
    print(nd[0], nd[1], nd[2])
    G.addEdge(nd[0], nd[1], nd[2])
    G.addEdge(nd[1], nd[0], nd[2])


print('1111',G)
start = G.getVertex('D')
prim(G, start)
print('2222',G)


#
# G = Graph()
# ndedge = [('v1', 'v2', 6), ('v1', 'v3', 1), ('v1', 'v4', 5),
#           ('v2', 'v3', 5), ('v3', 'v4', 5), ('v2', 'v5', 3),
#           ('v3', 'v5', 6), ('v3', 'v6', 4), ('v4', 'v6', 2),
#           ('v5', 'v6', 6)]
# for nd in ndedge:
#     G.addEdge(nd[0], nd[1], nd[2])
#     G.addEdge(nd[1], nd[0], nd[2])
# start = G.getVertex('v1')
# prim(G, start)
# print(G)
