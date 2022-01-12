
# ==============================================eno4j开源图库=====================================================
from py2neo import Graph, Node, Relationship
from py2neo.matching import *
# Graph()中第一个为local host链接，auth为认证，包含 username 和 password
gragh = Graph('http://localhost:7474',auth=('','123456789'))

# a = Node("hero", name="Clint")  # Node(label, name)
# b = Node("hero", name="Natasha")
# ab = Relationship(a, "friend", b)
# gragh.create(ab)  # 创建节点和关系
#
#

a = Node("region",name='HanDan')
b = Node("name",name='ZhangKe')
ab = Relationship(b,"born_of",a)
# gragh.create(ab)

# 该节点的id
# node_id = a.identity
# print(node_id)


# # 删除一个节点及与之相连的关系
# gragh.run('match (n:name{name:\'ZhangKe\'}) detach delete n')
# # 按照id删除节点
# gragh.run('match (r) where id(r) = 101 delete r')






# import py2neo
# from py2neo import *
# import pandas as pd
# print(py2neo.__version__)
# graph = Graph('http://localhost:7474',auth=('','123456789'))
# def yogadata():
#     count  = 0
#     frame = pd.read_csv(r"D:\\Gitlab\\my_world\\Work_Test\\Knowledge_Graph\\yoga.csv", encoding='gbk')
#     for i in frame.index:
#         '''获取数据'''
#         yoga_name = frame["招式"].values[i]
#         yoga_ms = frame["描述"].values[i]
#         yoga_yc = frame["益处"].values[i]
#         yoga_zysx = frame["注意事项"].values[i]
#         yoga_cjwt = frame["常见问题"].values[i]
#         # print(yoga_name)
#         # print(yoga_ms)
#         # print(yoga_yc)
#         # print(yoga_zysx)
#         # print(yoga_cjwt)
#
#         yoga_name = str(yoga_name)
#         yoga_ms = str(yoga_ms)
#         yoga_yc = str(yoga_yc)
#         yoga_zysx = str(yoga_zysx)
#         yoga_cjwt = str(yoga_cjwt)
#
#         '''
#             初始化实体
#         '''
#         yoga_node = Node('招式', name=yoga_name)
#         graph.merge(yoga_node)          ## merge方法是将重复数据去除掉，只留第一个
#         ms_node = Node('描述', name=yoga_ms)
#         yc_node = Node('益处', name=yoga_yc)
#         zysx_node = Node('注意事项', name=yoga_zysx)
#         cjwt_node = Node('常见问题', name=yoga_cjwt)
#
#         # 建造关系  瑜伽类
#         yoga_2 = Relationship(yoga_node, '描述', ms_node)
#         yoga_3 = Relationship(yoga_node, '益处', yc_node)
#         yoga_4 = Relationship(yoga_node, '注意事项', zysx_node)
#         yoga_5 = Relationship(yoga_node, '常见问题', cjwt_node)
#
#         try:
#             graph.create(yoga_2)
#         except:
#             continue
#         try:
#             graph.create(yoga_3)
#         except:
#             continue
#         try:
#             graph.create(yoga_4)
#         except:
#             continue
#         try:
#             graph.create(yoga_5)
#         except:
#             continue
#         count += 1
#         print(count)
# yogadata()
#
#





# ===================================================万象图调接口==========================================================
# import requests, json
# # github_url = "http://172.30.6.63:8080/graphs/{3ba65f8e1776a89b}/vertices?"
# github_url = "http://172.30.6.63:8080/graphs/3ba65f8e1776a89b/vertices"
# # data = json.dumps({'name':'test', 'description':'some test repo'})
# r = requests.get(github_url)
#
# print(r.json())
# # data = json.loads(r.json())
# # print(data)