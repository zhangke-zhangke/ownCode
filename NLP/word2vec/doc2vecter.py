# -*- coding: utf-8 -*-
import sys
import logging
import os
import gensim
import jieba
from jieba import posseg as pseg
import pandas as pd
# 引入doc2vec
from gensim.models import Doc2Vec

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

# 引入日志配置
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 加载数据
documents = []
# 使用count当做每个句子的“标签”，标签和每个句子是一一对应的
count = 0
with open('C:\\Users\\dell\\Desktop\\中共中央办公厅 国务院办公厅印发《关于加强金融服务民营企业的若干意见》.txt', 'r',encoding='gbk') as f:
    print(f.readline())
    file_list = []
    for line in f:
        if len(line.strip()) == 0:
            pass
        else:
            file_list.append(line.strip())
    result = []
    for sentence in file_list:
        sentence_word = jieba.cut(sentence)
        word = ' '.join(sentence_word).split()
        result.append(word)
        # result.append(' '.join(tuple(word)))
    print(result)

    # sys.exit()
    # title = unicode(line, 'utf-8')
    # # 切词，返回的结果是列表类型
    # words = ko_title2words(title)
    # 这里documents里的每个元素是二元组，具体可以查看函数文档
    for i in range(len(result)):
        documents.append(gensim.models.doc2vec.TaggedDocument(result[i], [str(i)]))
        if i % 10000 == 0:
            logging.info('{} has loaded...'.format(count))
    print(documents)


# 模型训练
model = Doc2Vec(documents, dm=1, vector_size=100, window=8, min_count=5, workers=4)
model.train(documents,total_examples=model.corpus_count,epochs=10)

# # 与标签0最相近的
# print(model.docvecs.most_similar('0'))
# # 两个标签的相关性比较
# print(model.docvecs.similarity('0','1'))
# # 标签为10的句子向量
# print(model.docvecs[10])
# # 输出词向量
# print(model['import'])
# # 推断句子向量 （未出现的训练中）
# print(model.infer_vector('今天 新建 了 一个 文档'.split()))

# todo : 找出相近短语
inferred_vector = model.infer_vector('加大金融政策支持力度，着力提升对民营企业金融服务的针对性和有效性'.split(),alpha=0.025,epochs=500)
similar_phrase = model.docvecs.most_similar([inferred_vector],topn=10)
print(similar_phrase)   # 标签 相似值
similar_result = []
for target,similar_value in similar_phrase:
    # print(target,similar_value)
    sentence = file_list[int(target)]
    print(sentence)
    similar_result.append([sentence,similar_value,len(sentence)])

final_result = pd.DataFrame(similar_result,columns=['相似段落','相似度','段落长度'])
print(final_result)

try:
    if os.path.exists('C:\\Users\\dell\\Desktop\\doc2vecter_result.csv'):
        print("已存在文件，先删除再操作")
        os.remove('C:\\Users\\dell\\Desktop\\doc2vecter_result.csv')
    else:
        print("写入数据到csv")
finally:
    try:
        final_result.to_csv('C:\\Users\\dell\\Desktop\\doc2vecter_result.csv', index=False)
    except Exception as e:
        print("写入失败，错误信息：",e)
    else:
        print("写入成功")

    # print("+++++++++++",sentence)
    # words = ''
    # for sen in sentence:
    #     print("===========",sen)
    #
    #     sys.exit()
    #     words += sen + ''
    # # print(words,similar_value,len(sentence))




# 保存模型
# model.save('models/ko_d2v.model')