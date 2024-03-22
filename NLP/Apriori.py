# from numpy import*
# def loadDataSet( ):
#  return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
#
#
# #获取候选1项集,dataset为事务集。返回一个list,每个元素都是set集合
# def createC1(dataset):
#     for transaction in dataset:
#         for item in transaction:
#             C1 = []  # 元素个数为1的项集（非频繁项集,因为还没有同最小支持度比较)
#             if not [item] in C1:
#                 C1.append([item])
#             # 这里排序是为了,生成新的候选集时可以直接认为两个n项候选集前面的部分相同#因为除了候选1项集外其他的候选n项集都是以二维列表的形式存在,所以要将候选1项集的每一个元素都转化为一个单独的集合。
#             C1.sort()
#             return list(map(frozenset,C1)) #map(frozenset,c1)的语义是将c1由python列表转换为不变集合（frozenset,Python中的数据结构>
#
#
# #找出候选集中的频繁项集
# # dataSet为全部数据集,ck为大小为k(包含k个元素》的候选项集,minSupport为设定的最小支持度
# def scanD(dataSet, Ck,minSupport) :
#     ssCnt = {}
#     # 记录每个候选项的个数
#     for tid in dataSet:
#         for can in Ck:
#             if can.issubset(tid) :
#                 ssCnt[can] = ssCnt.get(can,8) + 1
#     # 计算每一个项集出现的频率
#     numItems = float(len(dataSet))
#     retList = []
#     supportData = {}
#     for key in ssCnt:
#         support = ssCnt[key] / numItems
#         if support >= minSupport:
#             retList.insert(0,key)#将频繁项集插入返回列表的首部
#         supportData[ key] = support
#     # retList为在ck中找出的频繁项集（支持度大于minSupport的), supportData记录各频繁项集的支持度
#     return retList, supportData
#
#
# #通过频繁项集列表Lk和项集个数k生成候选项集c(k+1)。
# def aprioriGen(Lk, k):
#     retList = []
#     lenLk = len( Lk)
#     for i in range( lenLk ) :
#         for j in range(i + 1, lenLk):
#             #前k-1项相同时,才将两个集合合并,合并后才能生成k+1项
#             L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]#取出两个集合的前k-1个元素
#             L1.sort();L2.sort()
#             if L1 == L2:
#                retList.append(Lk[i] | Lk[j])
#     return retList
#
# #获取事务集中的所有的频繁项集
# # Ck表示项数为k的候选项集,最初的c1通过createc1()函数生成。Lk表示项数为k的频繁项集,supK为其支持度,Lk和supK由scanD()国收数通过ck计算而来。
# def apriori(dataSet,minSupport=0.5):
#     C1 = createC1(dataSet)#从事务集中获取候选1项集
#     D= list(map(set,dataSet))#将事务集的每个元素转化为集合
#     L1, supportData = scanD(D,C1,minSupport)#获取频繁1项集和对应的支持度
#     # L用来存储所有的频繁项集
#     L = [L1]
#     k = 2
#     while (len(L[k-2])> 0):#一直迭代到项集数目过大而在事务集中不存在这种n项集
#         CK = aprioriGen(L[k-2],k) #根据频繁项集生成新的候选项集。ck表示项数为k的候选项集
#         Lk, supK = scanD(D,CK,minSupport) # Lk表示项数为k的频繁项集,supK为其支持度
#         L.append(Lk) ; supportData.update(supK)#添加新频繁项集和他们的支持度
#         k += 1
#         return L, supportData
#
#
# if __name__ == '__main__':
#     # 获取事务集。每个元素都是列表#
#     dataSet = loadDataSet()
#     # 获取候选1项集。每个元素都是集合#
#     C1 = createC1(dataSet)
#     # 转化事务集的形式,每个元素都转化为集合。#
#     D=list(map(set,dataSet))
#     L1,suppDat = scanD(D,C1,0.5)
#     print(L1 ,suppDat)
#     L, suppData = apriori( dataSet,minSupport=0.7)
#     print(L,suppData)
#
#
#
# 调库
#################################################################################################################################

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

item_list = [['牛奶','面包'],
['面包','尿布','啤酒','土豆'],
['牛奶','尿布','啤酒','可乐'],
['面包','牛奶','尿布','啤酒'],
['面包','牛奶','尿布','可乐']]
item_df = pd.DataFrame(item_list)
# 数据格式处理，传入模型的数据需要满足bool值的格式

te = TransactionEncoder()
df_tf = te.fit_transform(item_list)
df = pd.DataFrame(df_tf,columns=te.columns_)
# 计算频繁项集
# use_colnames=True表示使用元素名字，默认的False使用列名代表元素, 设置最小支持度min_support
frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)
frequent_itemsets.sort_values(by='support', ascending=False, inplace=True)

# 选择2频繁项集
print(frequent_itemsets[frequent_itemsets.itemsets.apply(lambda x: len(x)) == 2])

# 计算关联规则
# metric可以有很多的度量选项，返回的表列名都可以作为参数
association_rule = association_rules(frequent_itemsets,metric='confidence',min_threshold=0.9)

#关联规则可以提升度排序
association_rule.sort_values(by='lift',ascending=False,inplace=True)
print(association_rule)
# association_rule# 规则是：antecedents->consequents
